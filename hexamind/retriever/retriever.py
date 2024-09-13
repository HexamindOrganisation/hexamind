import logging
from hexamind.database.adapters.AbstractDb import IDbClient
from hexamind.llm.llm.LlmAgent import LlmAgent
from hexamind.model.chunk.chunk import Chunk
import cohere
from typing import List, Dict, Any
import os
from collections import defaultdict

logger = logging.getLogger(__name__)

class Retriever:
    def __init__(self, db_client: IDbClient, llm_agent: LlmAgent):
        self.db_client = db_client
        self.llm_agent = llm_agent
        self.cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))
        logger.info("Retriever initialized with db_client and llm_agent")

    def similarity_search(self, query, condition) -> List[Chunk]:
        logger.info(f"Performing similarity search for query: {query}")
        query_dense_embedding = self.llm_agent.get_embedding(query)
        query_sparse_embedding = self.llm_agent.get_sparse_embedding(query)
        chunks = self.db_client.hybrid_search(
            query_dense_vector=query_dense_embedding,
            query_sparse_vector=query_sparse_embedding,
            num_results=50,
            condition=condition,
        )
        logger.debug(f"Similarity search returned {len(chunks)} chunks")
        return chunks

    def hybrid_search(self, query_dense_vector, query_sparse_vector, num_results=50, condition=None) -> List[Chunk]:
        logger.info(f"Performing hybrid search with num_results={num_results}")
        dense_results = self.db_client.search(query_dense_vector, "dense", num_results, condition)
        sparse_results = self.db_client.search(query_sparse_vector, "sparse", num_results, condition)
        
        logger.debug(f"Dense search returned {len(dense_results)} results")
        logger.debug(f"Sparse search returned {len(sparse_results)} results")

        rrf_scores = defaultdict(float)
        k = 60  # RRF constant

        for rank, result in enumerate(dense_results + sparse_results):
            chunk_id = result.id
            rrf_scores[chunk_id] += 1 / (k + rank)

        sorted_chunks = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
        
        top_chunks = []
        for chunk_id, _ in sorted_chunks[:num_results]:
            chunk = next((c for c in dense_results + sparse_results if c.id == chunk_id), None)
            if chunk:
                top_chunks.append(chunk)

        logger.info(f"Hybrid search returned {len(top_chunks)} top chunks")
        return top_chunks

    def reranker(self, query, chunks, top_n=30) -> List[Chunk]:
        logger.info(f"Reranking {len(chunks)} chunks with top_n={top_n}")
        if not chunks:
            logger.warning("No chunks to rerank")
            return []

        results = self.cohere_client.rerank(
            model="rerank-multilingual-v3.0",
            query=query,
            documents=[chunk.content for chunk in chunks],
            top_n=top_n,
        )

        reranked_chunks = []
        for i, r in enumerate(results.results):
            chunk = chunks[r.index]
            chunk.index = i + 1
            chunk.distance = r.relevance_score
            reranked_chunks.append(chunk)

        logger.debug(f"Reranker returned {len(reranked_chunks)} reranked chunks")
        return reranked_chunks

    def retrieve(self, query, condition: Dict[str, Any]) -> List[Chunk]:
        logger.info(f"Retrieving chunks for query: {query}")
        query_dense_embedding = self.llm_agent.get_embedding(query)
        query_sparse_embedding = self.llm_agent.get_sparse_embedding(query)
        
        hybrid_results = self.hybrid_search(
            query_dense_vector=query_dense_embedding,
            query_sparse_vector=query_sparse_embedding,
            num_results=50,
            condition=condition,
        )
        
        if hybrid_results:
            reranked_chunks = self.reranker(query, hybrid_results)
        else:
            logger.warning("No hybrid results found")
            reranked_chunks = []
        
        logger.info(f"Retrieved and reranked {len(reranked_chunks)} chunks")
        return reranked_chunks