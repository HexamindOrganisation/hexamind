from hexamind.model.model.element import Element
from hexamind.model.model.container import Container
from hexamind.model.model.block import Block
from hexamind.model.document import Document
from hexamind.database.adapters.AbstractDb import IDbClient
from hexamind.llm.llm.LlmAgent import LlmAgent
from hexamind.model.chunk.chunk import Chunk

class Ingestor:
    def __init__(self, db_client: IDbClient, llm_agent: LlmAgent):
        self.db_client = db_client
        self.llm_agent = llm_agent
    
    def ingest_content(self, document: Document, chunking = "semantic"):
        chunks = document.extract_chunks(strategy=chunking, max_tokens = 5000, threshold = 0.7)
        print(f'Chunks done')
        print(f'Ingesting {len(chunks)} chunks')
        for i, chunk in enumerate(chunks):
            print(f'Chunk: {i}')
            chunk.generate_embeddings(self.llm_agent)
            dict_chunk = chunk.to_vectorizzed_dict()
            self.db_client.add_document(
                document=dict_chunk['content'],
                dense_embedding=dict_chunk['dense_embeddings'],
                sparse_embedding=dict_chunk['sparse_embeddings'],
                ids=dict_chunk['id'],
                metadatas=dict_chunk['metadata']
            )
        print(f'Chunks stored')

