from typing import Optional, Dict, Any, List
from hexamind.llm.llm import LlmAgent
import uuid

class Chunk:
    def __init__(self, content: str, container_uid: str, title: Optional[str] = None, level: Optional[int] = None, document_title : Optional[str] = None, section_number: Optional[str] = None):
        self.uid = str(uuid.uuid4())
        self.content = content
        self.container_uid = container_uid
        self.title = title
        self.level = level
        self.document_title = document_title
        self.section_number = section_number
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
            'title': self.title,
            'level': self.level,
            'document_title': self.document_title,
            'section_number': self.section_number,
            'metadata': self.metadata
        }
    
    def __str__(self) -> str:
        return f"Chunk: {self.title} - section_number: {self.section_number} - level: {self.level} - content: {self.content[:30]}..."