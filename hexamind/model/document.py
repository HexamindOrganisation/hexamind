from typing import Optional, Dict, Any, Union, List, Callable
from hexamind.model.model.container import Container
from hexamind.model.model.block import Block
from hexamind.model.builder.MkBuilder import MkBuilder
from hexamind.model.chunk.chunk import Chunk
from hexamind.model.chunk.chunk_extractor import ChunkExtractor
from hexamind.model.chunk.tokenizer import Tokenizer
from hexamind.model.chunk.itokenizer import ITokenizer
import uuid


class Document:
    def __init__(
        self,
        uid,
        html_content: str,
        title: str,
        metadatas: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        self.uid = uid if uid else str(uuid.uuid4())
        self.root_container: Container = MkBuilder.from_htlm(
            htlm_content=html_content, document_title=title, metadatas=metadatas
        )
        self.title: str = title
        self.summarizer: Optional["Summarizer"] = None
        self.tokenizer: ITokenizer = Tokenizer()

    def get_root(self) -> Container:
        """Returns the root container of the document"""
        return self.root_container

    def get_title(self) -> str:
        """Returns the title of the document"""
        return self.title

    def set_summarizer(self, summarizer: "Summarizer") -> None:
        """
        Set the summarizer to be used for summarizing the content of the document"""
        self.summarizer = summarizer

    def set_tokenizer(self, tokenizer: ITokenizer) -> None:
        """
        Set the tokenizer to be used for tokenizing the content of the document"""
        self.tokenizer = tokenizer

    def get_content(self) -> str:
        """Returns the entire content of the document"""
        return self.root_container.get_content()

    def visualize_structure(self, filename: str = "document_structure") -> None:
        """Visualize the structure of the document"""
        self.root_container.visualize(filename=filename)

    def to_dict(self) -> Dict[str, Any]:
        """Returns the document as a dictionary"""
        return {
            "uid": self.uid,
            "title": self.title,
            "root_container": self.root_container.to_dict(),
        }

    def get_section_content(self, section_number: str) -> Optional[str]:
        """Returns the content of the section with the given section number"""
        container = self._find_container_by_section_number(
            self.root_container, section_number
        )
        return container.get_content() if container else None

    def _find_container_by_section_number(
        self, container: Container, section_number: str
    ) -> Optional[Container]:
        """Find the container with the given section number in the document tree"""
        if container.section_number == section_number:
            return container
        for child in container.children:
            if isinstance(child, Container):
                result = self._find_container_by_section_number(child, section_number)
                if result:
                    return result
        return None

    def get_summary(
        self, section_number: Optional[str] = None, level: Optional[int] = None
    ) -> Union[str, List[str]]:
        """Returns the summary of the section with the given section number or the summaries of all sections at the given level"""
        if not self.summarizer:
            raise ValueError(
                "Summarizer not set, Please set a summarizer before calling this method. document.set_summarizer(summarizer)"
            )

        if section_number and level is not None:
            raise ValueError("Only one of section_number or level can be provided")

        if section_number:
            container = self._find_container_by_section_number(
                self.root_container, section_number
            )
            if container:
                return self.summarizer.summarize(
                    container.get_content(), self.title, container.title
                )
        elif level is not None:
            summaries = []
            self._collect_summaries_at_level(self.root_container, level, summaries)
            return summaries
        return None

    def _collect_summaries_at_level(
        self, container: Container, level: int, summaries: List[str]
    ) -> None:
        """Collect summaries of all sections at the given level in the document tree"""
        if container.level == level:
            summaries.append(
                self.summarizer.summarize(
                    container.get_content(), self.title, container.title
                )
            )
        for child in container.children:
            if isinstance(child, Container):
                self._collect_summaries_at_level(child, level, summaries)

    def extract_chunks(
        self,
        strategy: str = "block",
        callback: Optional[Callable[[Container, str], List[Chunk]]] = None,
        **kwargs,
    ) -> List[Chunk]:
        """Extract chunks from the document based on the given strategy"""

        if strategy == "block":
            return ChunkExtractor.extract_by_block(
                self.root_container, self.title, self.uid, self.tokenizer
            )
        elif strategy == "level":
            return ChunkExtractor.extract_by_level(
                self.root_container, self.title, self.uid, self.tokenizer
            )
        elif strategy == "section_number":
            return ChunkExtractor.extract_by_section_number(
                self.root_container, self.title, self.uid, self.tokenizer
            )
        elif strategy == "semantic":
            return ChunkExtractor.semantic_chunking(
                self.root_container,
                self.title,
                self.uid,
                self.tokenizer,
                threshold=kwargs.get("threshold", 0.50),
                max_tokens=kwargs.get("max_tokens", 500),
            )
        elif strategy == "custom":
            if callback is None:
                raise ValueError("Callback must be provided when strategy is 'custom'")
            return ChunkExtractor.custom_extraction(
                self.root_container, self.title, self.uid, self.tokenizer, callback
            )

        else:
            raise ValueError(
                "Invalid strategy, valid values are 'block', 'level', 'section_number', 'custom'"
            )

    def __str__(self) -> str:
        """Returns the string representation of the document"""
        return self.root_container._get_structure_string()

    def save(self, filename: str) -> None:
        """Save the document to the given file"""
        content = self.get_content()
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
