from hxm_rag.model.modelv2.element import Element
from hxm_rag.model.modelv2.container import Container
from hxm_rag.model.modelv2.block import Block
from hxm_rag.model.modelv2.document import Document
from hxm_rag.database.adapters.AbstractDb import IDbClient
from hxm_rag.llm.llm.LlmAgent import LlmAgent

class Ingestor:
    def __init__(self, db_client: IDbClient, llm_agent: LlmAgent):
        self.db_client = db_client
        self.llm_agent = llm_agent

    def store_container(self, container: Container):

        if container.embeddings:
             for doc, embedding, id, metadata in zip(container.chunks, container.embeddings, container.chunk_ids, container.metadatas):
                self.db_client.add_document(
                    document=doc,
                    embedding=embedding,
                    ids=id,
                    metadatas=metadata
                )

        for child in container.children:
            if isinstance(child, Container):
                self.store_container(child)
    
    def store_container_summaries(self, container: Container):
        if container.summary_embeddings:
            for doc, embedding, id, metadata in zip(container.summary_chunks, container.summary_embeddings, container.summary_chunk_id, container.summary_metadatas):
                self.db_client.add_document(
                    document=doc,
                    embedding=embedding,
                    ids=id,
                    metadatas=metadata
                )
        
        for child in container.children:
            if isinstance(child, Container):
                self.store_container_summaries(child)
    
    def ingest_content(self, document: Document):
        document.root_container.get_embeddings(self.llm_agent)
        print(f'Embeddings done')
        self.store_container(document.root_container)

    def ingest_summaries(self, document: Document):
        document.root_container.get_summaries(self.llm_agent)
        print(f'Summaries done')
        self.store_container_summaries(document.root_container)
        
    
