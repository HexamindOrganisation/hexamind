from typing import Optional, Dict, Any, List, Callable
from hexamind.model.model.container import Container
from hexamind.model.model.block import Block
from hexamind.model.chunk.chunk import Chunk
from hexamind.model.chunk.itokenizer import ITokenizer

class ChunkExtractor:

    MAX_TOKENS = 8000

    @staticmethod
    def slipt_content_into_chunks(content: str, 
                                  container_uid: str, 
                                  title: str, 
                                  level: int,
                                  document_title: str,
                                  section_number: str,
                                  tokenizer: ITokenizer) -> List[Chunk]:
        """Split the content into chunks of at most MAX_TOKENS tokens"""

        chunks = []
        tokens = tokenizer.tokenize(content)
        num_chunks = (len(tokens) + ChunkExtractor.MAX_TOKENS - 1) // ChunkExtractor.MAX_TOKENS

        for i in range(num_chunks):
            start_idx = i * ChunkExtractor.MAX_TOKENS
            end_ids = start_idx + ChunkExtractor.MAX_TOKENS
            chunk_content = tokenizer.decode(tokens[start_idx:end_ids])
            chunk = Chunk(
                content=chunk_content,
                container_uid=container_uid,
                title=title,
                level=level,
                document_title=document_title,
                section_number=section_number
            )
            chunks.append(chunk)
        return chunks

    @staticmethod
    def extract_by_block(container: Container, document_title : str, tokenizer: ITokenizer) -> List[Chunk]:
        """Extract a chunk for each block in the document"""

        chunks = []
        for child in container.children:
            if isinstance(child, Block):
                block_content = child.get_content()
                block_chunks = ChunkExtractor.slipt_content_into_chunks(
                    content=block_content,
                    container_uid=container.uid,
                    title=container.title,
                    level=container.level,
                    document_title=document_title,
                    section_number=container.section_number,
                    tokenizer=tokenizer
                )
                chunks.extend(block_chunks)
            elif isinstance(child, Container):
                chunks.extend(ChunkExtractor.extract_by_block(child, document_title, tokenizer))
        return chunks
    
    @staticmethod
    def extract_by_level(container: Container, level: int, document_title: str, tokenizer: ITokenizer) -> List[Chunk]:
        """Extract a chunk for each container at the given level"""
        chunks = []
        if container.level == level:
            container_content = container.get_content()
            container_chunks = ChunkExtractor.slipt_content_into_chunks(
                content=container_content,
                container_uid=container.uid,
                title=container.title,
                level=container.level,
                document_title=document_title,
                section_number=container.section_number,
                tokenizer=tokenizer
            )
            chunks.extend(container_chunks)
        for child in container.children:
            if isinstance(child, Container):
                chunks.extend(ChunkExtractor.extract_by_level(child, level, document_title))
        return chunks
    
    @staticmethod
    def extract_by_section_number(container: Container, section_number: str, document_title: str, tokenizer: ITokenizer) -> Optional[Chunk]:
        """Extract a chunk for the container with the given section number"""
        if container.section_number == section_number:
            container_content = container.get_content()
            return ChunkExtractor.slipt_content_into_chunks(
                content=container_content,
                container_uid=container.uid,
                title=container.title,
                level=container.level,
                document_title=document_title,
                section_number=container.section_number,
                tokenizer=tokenizer
            )
        for child in container.children:
            if isinstance(child, Container):
                chunk = ChunkExtractor.extract_by_section_number(child, section_number, document_title)
                if chunk:
                    return chunk
        return None
    
    @staticmethod
    def custom_extraction(container: Container, document_title: str, tokenizer: ITokenizer, callback: Callable[[Container, str], List[Chunk]]) -> List[Chunk]:
        """Extract chunks using a custom callback function"""
        return callback(container, document_title)