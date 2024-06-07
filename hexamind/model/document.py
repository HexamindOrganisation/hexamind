from typing import Optional, Dict, Any, Union, List, Callable
from hexamind.model.model.container import Container
from hexamind.model.model.block import Block
from hexamind.model.builder.MkBuilder import MkBuilder
from hexamind.model.chunk.chunk import Chunk
from hexamind.model.chunk.chunk_extractor import ChunkExtractor
from hexamind.model.chunk.tokenizer import Tokenizer
from hexamind.model.chunk.itokenizer import ITokenizer

class Document:
    def __init__(self, markdown_content : str, title: str):
        self.root_container : Container = MkBuilder.from_markdown(markdown_content=markdown_content, document_title=title)
        self.title : str = title
        self.summarizer : Optional['Summarizer'] = None
        self.tokenizer : ITokenizer = Tokenizer()
        
    
    def set_summarizer(self, summarizer: 'Summarizer') -> None:
        self.summarizer = summarizer
    
    def set_tokenizer(self, tokenizer: ITokenizer) -> None:
        self.tokenizer = tokenizer

    def get_content(self) -> str:
        """Returns the entire content of the document"""
        return self.root_container.get_content()

    def visualize_structure(self, filename: str = 'document_structure') -> None : 
        self.root_container.visualize(filename=filename)
    
    def to_dict(self) -> Dict[str, Any]:
        return self.root_container.to_dict()

    def get_section_content(self, section_number :str) -> Optional[str]:
        container = self._find_container_by_section_number(self.root_container, section_number)
        return container.get_content() if container else None

    def _find_container_by_section_number(self, container : Container, section_number: str) -> Optional[Container]:
        if container.section_number == section_number:
            return container
        for child in container.children:
            if isinstance(child, Container):
                result = self._find_container_by_section_number(child, section_number)
                if result:
                    return result
        return None
    
    def get_summary(self, section_number: Optional[str] = None, level: Optional[int] = None) -> Union[str, List[str]]:
        if not self.summarizer:
            raise ValueError("Summarizer not set, Please set a summarizer before calling this method. document.set_summarizer(summarizer)")
        
        if section_number and level is not None:
            raise ValueError("Only one of section_number or level can be provided")
        
        if section_number:
            container = self._find_container_by_section_number(self.root_container, section_number)
            if container: 
                return self.summarizer.summarize(container.get_content(), self.title, container.title)
        elif level is not None:
            summaries = []
            self._collect_summaries_at_level(self.root_container, level, summaries)
            return summaries
        return None
    
    def _collect_summaries_at_level(self, container: Container, level: int, summaries: List[str]) -> None:
        if container.level == level:
            summaries.append(self.summarizer.summarize(container.get_content(), self.title, container.title))
        for child in container.children:
            if isinstance(child, Container):
                self._collect_summaries_at_level(child, level, summaries)
    
    def extract_chunks(self, 
                       strategy: str = "block", 
                       level: Optional[int] = None, 
                       section_number: Optional[str] = None, 
                       callback : Optional[Callable[[Container, str], List[Chunk]]] = None) -> List[Chunk]:
        
        if strategy == "block":
            return ChunkExtractor.extract_by_block(self.root_container, self.title, self.tokenizer)
        elif strategy == "level":
            if level is None:
                raise ValueError("Level must be provided when strategy is 'level'")
            return ChunkExtractor.extract_by_level(self.root_container, level, self.title, self.tokenizer)
        elif strategy == "section_number":
            if section_number is None:
                raise ValueError("Section number must be provided when strategy is 'section_number'")
            chunk = ChunkExtractor.extract_by_section_number(self.root_container, section_number, self.title, self.tokenizer)
            return [chunk] if chunk else []
        elif strategy == "custom":
            if callback is None:
                raise ValueError("Callback must be provided when strategy is 'custom'")
            return ChunkExtractor.custom_extraction(self.root_container, self.title, self.tokenizer, callback)
        
        else:
            raise ValueError("Invalid strategy, valid values are 'block', 'level', 'section_number', 'custom'")
        
    def __str__(self) -> str:
        return f"Document: {self.title}\nContent:\n{self.get_content()}"
    
    def save(self, filename: str) -> None:
        content = self.get_content()
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)