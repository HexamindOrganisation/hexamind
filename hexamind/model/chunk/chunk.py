from typing import Optional, Dict, Any, List
from hexamind.llm.llm import LlmAgent
import uuid

class Chunk:
    def __init__(self, content: str, container_uid: str, document_uid: str, title: Optional[str] = None, level: Optional[int] = None, document_title : Optional[str] = None, section_number: Optional[str] = None, index: Optional[int] = None, distance: Optional[float] = None) -> None:
        self.uid = str(uuid.uuid4())
        self.content = content
        self.container_uid = container_uid
        self.document_uid = document_uid
        self.title = title
        self.level = level
        self.document_title = document_title
        self.section_number = section_number
        self.index = index
        self.distance = distance
        self.embeddings: Optional[List[float]] = None
        self.metadata: Dict[str, Any] = {}

    def add_metadata(self, key: str, value: Any) -> None:
        self.metadata[key] = value

    def generate_embeddings(self, ll_agent: LlmAgent) -> None:
        self.embeddings = ll_agent.get_embedding(self.content)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'content': self.content,
            'container_uid': self.container_uid,
            'document_uid': self.document_uid,
            'title': self.title,
            'level': self.level,
            'document_title': self.document_title,
            'section_number': self.section_number,
            'index': self.index,
            'distance': self.distance,
            'metadata': self.metadata
        }
    
    def to_vectorizzed_dict(self) -> Dict[str, Any]:
        return {
            'content': self.content,
            'embeddings': self.embeddings,
            'id': self.uid,
            'metadata': {
                'document_title': self.document_title if self.document_title is not None else '',
                'content': self.content,
                'container_uid': self.container_uid,
                'document_uid': self.document_uid,
                'title': self.title if self.title is not None else '',
                'level': self.level if self.level is not None else 0,
                'section_number': self.section_number if self.section_number is not None else '',
                'index': self.index if self.index is not None else 0,
                'distance': self.distance if self.distance is not None else 0,
                'metadata': self.metadata if self.metadata else ''
            }

        }
    
    def __str__(self) -> str:
        return f"Chunk: {self.title} - section_number: {self.section_number} - level: {self.level} - content: {self.content[:30]}..."