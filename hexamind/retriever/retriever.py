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
        chunks = self.db_client.hybrid_search(query_dense_vector=query_dense_embedding,query_sparse_vector=query_sparse_embedding, num_results=50, condition=condition)
        return chunks
    
    def reranker(self, query, chunks, top_n = 30) -> List[Chunk]:
        results = self.cohere_client.rerank(
            model="rerank-multilingual-v3.0",
            query = query,
            documents = [chunk.content for chunk in chunks],
            top_n=top_n)
        # retrurn the reranked chunks
        relevant_scores = [r.relevance_score for r in results.results]
        if not relevant_scores:
            return []
        threshold = np.percentile(relevant_scores, 90)
        print(f"Threshold: {threshold}")
        resorted_results = []
        for idx, r in enumerate(results.results):
            if (r.relevance_score >= threshold):
                resorted_results.append((r.index, r.relevance_score))
        reranked_chunks = []
        for i, result in enumerate(resorted_results):
            chunks[result[0]].index = i+1
            chunks[result[0]].distance = result[1]
            reranked_chunks.append(chunks[result[0]])
        print(reranked_chunks)
        return reranked_chunks


    def retrieve(self, query, condition: Dict[str,Any]) -> List[Chunk]:
        #condition = self._create_condition(folder)
        chunks = self.similarity_search(query, condition=condition)
        if len(chunks) > 0:
            reranked_chunks = self.reranker(query, chunks)
        else:
            reranked_chunks = []
        return reranked_chunks