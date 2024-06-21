from hexamind.database.adapters.AbstractDb import IDbClient
from hexamind.llm.llm.LlmAgent import LlmAgent
from hexamind.model.chunk.chunk import Chunk
import cohere
from typing import List
import os

class Retriever: 
    def __init__(self, db_client: IDbClient, llm_agent: LlmAgent):
        self.db_client = db_client
        self.llm_agent = llm_agent
        self.cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))
    
    def similarity_search(self, query, condition) -> List[Chunk]:
        query_embedding = self.llm_agent.get_embedding(query)
        results = self.db_client.search(query_embedding, num_results=2000, condition=condition)
        print(results)
        contents = results['documents'][0]
        metadatas = results['metadatas'][0]

        chunks = []
        for content, metadata in zip(contents, metadatas):
            chunk = Chunk(content, metadata['container_uid'], metadata['document_uid'], metadata['title'], metadata['level'], metadata['document_title'], metadata['section_number'], metadata['index'], metadata['distance'])
            chunks.append(chunk)
        return chunks
    
    def reranker(self, query, chunks, top_n = 30, return_n = 10) -> List[Chunk]:
        results = self.cohere_client.rerank(
            model="rerank-multilingual-v3.0",
            query = query, 
            documents = [chunk.content for chunk in chunks],
            top_n=top_n)
        
        # retrurn the reranked chunks

        resorted_index = []
        for idx, r in enumerate(results.results):
            if (r.relevance_score > 0.85) & (len(resorted_index)< return_n):
                resorted_index.append(r.index)

        reranked_chunks = [chunks[i] for i in resorted_index]

        return reranked_chunks


    def retrieve(self, query, condition: dict) -> List[Chunk]:
        chunks = self.similarity_search(query, condition=condition)
        reranked_chunks = self.reranker(query, chunks)
        return reranked_chunks
    
    def _create_condition(selected_documents: List[str]) -> dict:
        if selected_documents:
            return {
                'document_title': {"$in": selected_documents}
            }
        return {}