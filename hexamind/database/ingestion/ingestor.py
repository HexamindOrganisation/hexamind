import logging
from hexamind.model.model.element import Element
from hexamind.model.model.container import Container
from hexamind.model.model.block import Block
from hexamind.model.document import Document
from hexamind.database.adapters.AbstractDb import IDbClient
from hexamind.llm.llm.LlmAgent import LlmAgent
from hexamind.model.chunk.chunk import Chunk
from typing import List, Dict, Any, Optional
from hexamind.utils.config.ingestor import IngestorConfig

logger = logging.getLogger(__name__)


class Ingestor:
    def __init__(self, db_client: IDbClient, 
                 llm_agent: LlmAgent,
                 config: IngestorConfig = None):
        self.db_client = db_client
        self.llm_agent = llm_agent
        self.config = config or IngestorConfig()

    def ingest_content(self, 
                       document: Document, 
                       chunking: str = "semantic" #TODO: unused, need to remove after verification
                       ):
        logger.info(f"Ingesting document: {document}")
        chunks = document.extract_chunks(
            strategy=self.config.chunking_strategy, 
            max_tokens=self.config.max_tokens_per_chunk, 
            threshold=self.config.semantic_chunking_threshold
        )
        logger.debug("Chunk extraction completed")
        logger.info(f"Ingesting {len(chunks)} chunks")
        for i, chunk in enumerate(chunks):
            logger.debug(f"Processing chunk: {i}")
            chunk.generate_embeddings(self.llm_agent)
            dict_chunk = chunk.to_vectorizzed_dict()
            logger.debug(f"Chunk metadata: {chunk.metadatas}")
            self.db_client.add_document(
                document=dict_chunk["content"],
                dense_embedding=dict_chunk["dense_embeddings"],
                sparse_embedding=dict_chunk["sparse_embeddings"],
                ids=dict_chunk["id"],
                metadatas=dict_chunk["metadata"],
            )
        logger.info("Chunk ingestion completed")
