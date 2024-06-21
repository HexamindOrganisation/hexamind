from hexamind.database.adapters.AbstractDb import IDbClient
from hexamind.llm.llm.LlmAgent import LlmAgent
from hexamind.model.chunk.chunk import Chunk
import cohere
from typing import List, Dict, Any
import os
import json

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
    
    def reranker(self, query, chunks, top_n = 30) -> List[Chunk]:
        results = self.cohere_client.rerank(
            model="rerank-multilingual-v3.0",
            query = query, 
            documents = [chunk.content for chunk in chunks],
            top_n=top_n)
        
        # retrurn the reranked chunks

        resorted_results = []
        for idx, r in enumerate(results.results):
            if (r.relevance_score > 0.85):
                resorted_results.append((r.index, r.relevance_score))

        reranked_chunks = []
        for i, result in enumerate(resorted_results):
            chunks[result[0]].index = i+1
            chunks[result[0]].distance = result[1]
            reranked_chunks.append(chunks[result[0]])

        return reranked_chunks


    def retrieve(self, query, folder: str) -> List[Chunk]:
        condition = self._create_condition(folder)
        chunks = self.similarity_search(query, condition=condition)
        reranked_chunks = self.reranker(query, chunks)
        return reranked_chunks
    
    def _create_condition(self, folder: str) -> Dict[str, Any]:
        with open("folders.json", 'r') as file:
            json_of_folders = json.load(file)
        files_for_folder = [f["files"] for f in json_of_folders["entries"] if f["name"] == folder]
        condition = {"document_title": {"$in": [file for sublist in files_for_folder for file in sublist]}}
        return condition