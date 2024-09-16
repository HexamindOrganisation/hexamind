import logging
from hexamind.database.adapters.AbstractDb import IDbClient
from hexamind.llm.llm.LlmAgent import LlmAgent
from hexamind.model.chunk.chunk import Chunk
import cohere
from typing import List, Dict, Any
import os
from collections import defaultdict
import numpy as np
from hexamind.utils.config.retriever import RetrieverConfig

logger = logging.getLogger(__name__)

class Retriever:
    def __init__(self, 
                 db_client: IDbClient, 
                 llm_agent: LlmAgent, 
                 config: RetrieverConfig = None
                 ):
        self.db_client = db_client
        self.llm_agent = llm_agent
        self.config = config or RetrieverConfig()
        self.cohere_client = cohere.Client(self.config.cohere_api_key)
        logger.info("Retriever initialized with db_client, llm_agent, and config")

    def similarity_search(self, 
                          query, 
                          condition
                          ) -> List[Chunk]:
        logger.info(f"Performing similarity search for query: {query}")
        query_dense_embedding = self.llm_agent.get_embedding(query)
        query_sparse_embedding = self.llm_agent.get_sparse_embedding(query)
        chunks = self.db_client.hybrid_search(
            query_dense_vector=query_dense_embedding,
            query_sparse_vector=query_sparse_embedding,
            num_results=self.config.max_hybrid_search_results,
            condition=condition,
        )
        logger.debug(f"Similarity search returned {len(chunks)} chunks")
        return chunks

    def hybrid_search(
        self, 
        query_dense_vector, 
        query_sparse_vector, 
        condition=None
    ) -> List[Chunk]:
        logger.info(f"Performing hybrid search with num_results={self.config.max_hybrid_search_results}")
        dense_results = self.db_client.search(
            query_dense_vector, "dense", self.config.max_hybrid_search_results, condition
        )
        sparse_results = self.db_client.search(
            query_sparse_vector, "sparse", self.config.max_hybrid_search_results, condition
        )

        logger.debug(f"Dense search returned {len(dense_results)} results")
        logger.debug(f"Sparse search returned {len(sparse_results)} results")

        rrf_scores = defaultdict(float)

        for rank, result in enumerate(dense_results + sparse_results):
            chunk_id = f"{result.document_uid}_{result.index}"
            rrf_score = 1 / (self.config.rrf_k + rank)
            rrf_scores[chunk_id] += rrf_score
            logger.debug(f"Chunk {chunk_id} got RRF score: {rrf_score}")

        sorted_chunks = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
        logger.debug(f"Sorted chunks: {sorted_chunks}")

        top_chunks = []
        for chunk_id, score in sorted_chunks[:self.config.max_hybrid_search_results]:
            parts = chunk_id.rsplit('_', 1)
            if len(parts) == 2:
                doc_uid, index = parts
                try:
                    index = int(index)
                    chunk = next(
                        (c for c in dense_results + sparse_results if c.document_uid == doc_uid and c.index == index),
                        None
                    )
                    if chunk:
                        chunk.distance = score  # Update the distance with the RRF score
                        top_chunks.append(chunk)
                        logger.debug(f"Added chunk {chunk_id} with score {score}")
                except ValueError:
                    logger.warning(f"Invalid index in chunk_id: {chunk_id}")
            else:
                logger.warning(f"Invalid chunk_id format: {chunk_id}")

        logger.info(f"Hybrid search returned {len(top_chunks)} top chunks")
        return top_chunks

    def reranker(self, 
                 query, 
                 chunks
                 ) -> List[Chunk]:
        logger.info(f"Reranking {len(chunks)} chunks")
        if not chunks:
            logger.warning("No chunks to rerank")
            return []

        results = self.cohere_client.rerank(
            model=self.config.rerank_model,
            query=query,
            documents=[chunk.content for chunk in chunks],
            top_n=self.config.max_rerank_results,
        )

        reranked_chunks = []
        for i, r in enumerate(results.results):
            chunk = chunks[r.index]
            chunk.index = i + 1
            chunk.distance = r.relevance_score
            reranked_chunks.append(chunk)

        logger.debug(f"Reranker returned {len(reranked_chunks)} reranked chunks")
        return reranked_chunks

    def peloton_selection(self, 
                          chunks: List[Chunk]
                          ) -> List[Chunk]:
        if not chunks:
            return []

        sorted_chunks = sorted(chunks, key=lambda x: x.distance, reverse=True)
        scores = np.array([chunk.distance for chunk in sorted_chunks])
        n = len(scores)

        diffs = np.diff(scores)
        mean_diff = np.mean(diffs)
        std_diff = np.std(diffs)

        threshold = mean_diff + self.config.peloton_beta * std_diff
        cut_index = next((i for i, diff in enumerate(diffs) if diff > threshold), n - 1)

        min_size = max(int(self.config.peloton_alpha * n), self.config.min_chunks_to_return)
        max_size = min(self.config.max_chunks_to_return, n)
        cut_index = max(min(cut_index, max_size), min_size)

        logger.info(f"Peloton algorithm selected {cut_index} chunks out of {n}")
        return sorted_chunks[:cut_index]

    def retrieve(self, 
                 query, 
                 condition: Dict[str, Any]
                 ) -> List[Chunk]:
        logger.info(f"Retrieving chunks for query: {query}")
        query_dense_embedding = self.llm_agent.get_embedding(query)
        query_sparse_embedding = self.llm_agent.get_sparse_embedding(query)

        hybrid_results = self.hybrid_search(
            query_dense_vector=query_dense_embedding,
            query_sparse_vector=query_sparse_embedding,
            condition=condition,
        )

        if hybrid_results:
            reranked_chunks = self.reranker(query, hybrid_results)
            selected_chunks = self.peloton_selection(reranked_chunks)
            
            # Filter chunks based on the relevance threshold from config
            relevant_chunks = [chunk for chunk in selected_chunks if chunk.distance >= self.config.relevance_threshold]
            
            if relevant_chunks:
                logger.info(f"Retrieved, reranked, and selected {len(relevant_chunks)} relevant chunks")
                return relevant_chunks
            else:
                logger.warning(f"No chunks met the relevance threshold of {self.config.relevance_threshold}")
                return []
        else:
            logger.warning("No hybrid results found")
            return []