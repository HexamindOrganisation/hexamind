from typing import Optional, Dict, Any, List, Callable
from hexamind.model.model.container import Container
from hexamind.model.model.block import Block
from hexamind.model.chunk.chunk import Chunk
from hexamind.model.chunk.itokenizer import ITokenizer
from sentence_transformers import SentenceTransformer, util

import stanza

stanza.download("fr")


class ChunkExtractor:

    MAX_TOKENS = 1500
    OVERLAP_TOKENS = 200

    @staticmethod
    def _slipt_content_into_chunks(
        content: str,
        container_uid: str,
        document_uid: str,
        title: str,
        level: int,
        document_title: str,
        section_number: str,
        metadata: Optional[List[Dict[str, Any]]],
        tokenizer: ITokenizer,
        overlap: int = OVERLAP_TOKENS,
    ) -> List[Chunk]:
        """Split the content into chunks of at most MAX_TOKENS tokens"""

        chunks = []
        tokens = tokenizer.tokenize(text=content)
        num_chunks = (
            len(tokens) + ChunkExtractor.MAX_TOKENS - 1
        ) // ChunkExtractor.MAX_TOKENS

        for i in range(num_chunks):
            start_idx = max(0, i * (ChunkExtractor.MAX_TOKENS - overlap))
            end_ids = min(len(tokens), start_idx + ChunkExtractor.MAX_TOKENS)
            chunk_content = tokenizer.decode(tokens[start_idx:end_ids])
            chunk = Chunk(
                content=chunk_content,
                container_uid=container_uid,
                document_uid=document_uid,
                title=title,
                level=level,
                document_title=document_title,
                section_number=section_number,
                index=i,
                metadatas=metadata,
            )
            chunks.append(chunk)
        return chunks

    @staticmethod
    def extract_by_block(
        container: Container,
        document_title: str,
        document_uid: str,
        tokenizer: ITokenizer,
    ) -> List[Chunk]:
        """Extract a chunk for each block in the document"""

        chunks = []
        for child in container.children:
            if isinstance(child, Block):
                block_content = child.get_content()
                block_chunks = ChunkExtractor._slipt_content_into_chunks(
                    content=block_content,
                    container_uid=container.uid,
                    document_uid=document_uid,
                    title=container.title,
                    level=container.level,
                    document_title=document_title,
                    section_number=child.section_number,
                    metadata=child.metadatas,
                    tokenizer=tokenizer,
                )
                chunks.extend(block_chunks)
            elif isinstance(child, Container):
                chunks.extend(
                    ChunkExtractor.extract_by_block(
                        child, document_title, document_uid, tokenizer
                    )
                )
        return chunks

    @staticmethod
    def extract_by_level(
        container: Container,
        document_title: str,
        document_uid: str,
        tokenizer: ITokenizer,
    ) -> List[Chunk]:
        """Extract a chunk for each container at the given level"""
        chunks = []
        levels = ChunkExtractor.get_levels(container)
        for level in levels:
            chunks.extend(
                ChunkExtractor._extract_chunks_for_level(
                    container, level, document_title, document_uid, tokenizer
                )
            )
        return chunks

    @staticmethod
    def extract_by_section_number(
        container: Container,
        document_title: str,
        document_uid: str,
        tokenizer: ITokenizer,
    ) -> List[Chunk]:
        """Extract a list of chunk where a chunk represents a section number"""
        chunks = []
        section_numbers = ChunkExtractor.get_section_numbers(container)
        for section_number in section_numbers:
            chunks.extend(
                ChunkExtractor._extract_chunks_for_section(
                    container, section_number, document_title, document_uid, tokenizer
                )
            )
        return chunks

    @staticmethod
    def get_section_numbers(container: Container) -> List[str]:
        """Get the section numbers of the containers in the document tree"""
        section_numbers = set()
        if container.children:
            for child in container.children:
                if isinstance(child, Container):
                    section_numbers.add(child.section_number)
                    section_numbers.update(ChunkExtractor.get_section_numbers(child))
        return list(section_numbers)

    @staticmethod
    def _extract_chunks_for_section(
        container: Container,
        section_number: str,
        document_title: str,
        document_uid: str,
        tokenizer: ITokenizer,
    ) -> List[Chunk]:
        """Extract chunks for the container with the given section number"""
        chunks = []
        if container.section_number == section_number:
            container_content = container.get_content()
            container_chunks = ChunkExtractor._slipt_content_into_chunks(
                content=container_content,
                container_uid=container.uid,
                document_uid=document_uid,
                title=container.title,
                level=container.level,
                document_title=document_title,
                section_number=container.section_number,
                metadata=container.metadatas,
                tokenizer=tokenizer,
            )
            chunks.extend(container_chunks)
        for child in container.children:
            if isinstance(child, Container):
                chunks.extend(
                    ChunkExtractor._extract_chunks_for_section(
                        child, section_number, document_title, document_uid, tokenizer
                    )
                )
        return chunks

    @staticmethod
    def get_levels(container: Container) -> List[int]:
        """Get the levels of the containers in the document tree"""
        levels = set()
        if container.children:
            for child in container.children:
                if isinstance(child, Container):
                    levels.add(child.level)
                    levels.update(ChunkExtractor.get_levels(child))
        return sorted(levels)

    @staticmethod
    def _extract_chunks_for_level(
        container: Container,
        level: int,
        document_title: str,
        document_uid: str,
        tokenizer: ITokenizer,
    ) -> List[Chunk]:
        """Extract chunks for the containers at the given level"""
        chunks = []
        if container.level == level:
            container_content = container.get_content()
            container_chunks = ChunkExtractor._slipt_content_into_chunks(
                content=container_content,
                container_uid=container.uid,
                document_uid=document_uid,
                title=container.title,
                level=container.level,
                document_title=document_title,
                section_number=container.section_number,
                metadata=container.metadatas,
                tokenizer=tokenizer,
            )
            chunks.extend(container_chunks)
        for child in container.children:
            if isinstance(child, Container):
                chunks.extend(
                    ChunkExtractor._extract_chunks_for_level(
                        child, level, document_title, document_uid, tokenizer
                    )
                )
        return chunks

    @staticmethod
    def semantic_chunking(
        container: Container,
        document_title: str,
        document_uid: str,
        tokenizer: ITokenizer,
        max_tokens: int = MAX_TOKENS,
        threshold: float = 0.80,
    ) -> List[Chunk]:
        """Extract chunks using semantic similarity at root_container level"""
        chunks = []
        content = container.get_content()
        sentences = _split_sentences(content)
        model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
        sentence_embeddings = model.encode(sentences, convert_to_tensor=True)
        current_chunk = ""
        current_tokens = 0
        current_embedding = None

        for i, sentence in enumerate(sentences):
            sentence_token = tokenizer.tokenize(sentence)
            sentence_embedding = sentence_embeddings[i]

            if current_tokens + len(sentence_token) > max_tokens or (
                current_embedding is not None
                and util.pytorch_cos_sim(current_embedding, sentence_embedding)
                < threshold
            ):
                chunk = Chunk(
                    content=current_chunk.strip(),
                    container_uid=container.uid,
                    document_uid=document_uid,
                    title=container.title,
                    level=container.level,
                    document_title=document_title,
                    section_number=container.section_number,
                    index=i,
                    metadatas=container.metadatas,
                )
                chunks.append(chunk)
                current_chunk = sentence
                current_tokens = len(sentence_token)
                current_embedding = sentence_embedding
            else:
                current_chunk += " " + sentence
                current_tokens += len(sentence_token)
                if current_embedding is None:
                    current_embedding = sentence_embedding
                else:
                    current_embedding = (
                        current_embedding * (current_tokens - len(sentence_token))
                        + +sentence_embedding * len(sentence_token)
                    ) / current_tokens

        if current_chunk:
            chunk = Chunk(
                content=current_chunk.strip(),
                container_uid=container.uid,
                document_uid=document_uid,
                title=container.title,
                level=container.level,
                document_title=document_title,
                section_number=container.section_number,
                index=len(sentences),
                metadatas=container.metadatas,
            )
            chunks.append(chunk)

        return chunks

    @staticmethod
    def custom_extraction(
        container: Container,
        document_title: str,
        document_uid: str,
        tokenizer: ITokenizer,
        callback: Callable[[Container, str], List[Chunk]],
    ) -> List[Chunk]:
        """Extract chunks using a custom callback function"""
        return callback(container, document_title, document_uid, tokenizer)


def _split_sentences(text):
    nlp = stanza.Pipeline("fr", processors="tokenize")
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sentences]
    return sentences
