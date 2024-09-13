from hexamind.database.adapters.AbstractDb import IDbClient
from hexamind.llm.llm.LlmAgent import LlmAgent
from hexamind.model.chunk.chunk import Chunk
import cohere
from typing import List, Dict, Any
import os
import json
import numpy as np


class Retriever:
    def __init__(self, db_client: IDbClient, llm_agent: LlmAgent):
        self.db_client = db_client
        self.llm_agent = llm_agent
        self.cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))

    def similarity_search(self, query, condition) -> List[Chunk]:
        query_dense_embedding = self.llm_agent.get_embedding(query)
        query_sparse_embedding = self.llm_agent.get_sparse_embedding(query)
        chunks = self.db_client.hybrid_search(
            query_dense_vector=query_dense_embedding,
            query_sparse_vector=query_sparse_embedding,
            num_results=50,
            condition=condition,
        )
        return chunks

    def reranker(self, query, chunks, top_n=30) -> List[Chunk]:
        results = self.cohere_client.rerank(
            model="rerank-multilingual-v3.0",
            query=query,
            documents=[chunk.content for chunk in chunks],
            top_n=top_n,
        )

        relevant_scores = [r.relevance_score for r in results.results]

        if not relevant_scores:
            return []

        threshold = np.percentile(relevant_scores, 70)
        print(f"Threshold: {threshold}")

        resorted_results = {}
        for r in results.results:
            if r.relevance_score >= threshold:
                if (
                    r.index not in resorted_results
                    or r.relevance_score > resorted_results[r.index]
                ):
                    resorted_results[r.index] = r.relevance_score

        reranked_chunks = []
        for i, (index, score) in enumerate(
            sorted(resorted_results.items(), key=lambda x: x[1], reverse=True)
        ):
            chunk = chunks[index]
            chunk.index = i + 1
            chunk.distance = score
            reranked_chunks.append(chunk)

        print(reranked_chunks)
        print("-------------------")
        for chunk in reranked_chunks:
            print(chunk.container_uid)

        return reranked_chunks

    def retrieve(self, query, condition: Dict[str, Any]) -> List[Chunk]:
        chunks = self.similarity_search(query, condition=condition)
        print(chunks)
        if chunks:
            reranked_chunks = self.reranker(query, chunks)
        else:
            reranked_chunks = []
        return reranked_chunks
