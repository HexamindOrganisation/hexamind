from hxm_rag.model.modelv2.element import Element
from hxm_rag.llm.llm.LlmAgent import LlmAgent
import uuid

class UIDWrapper:
    def __init__(self, uid, level=None):
        self.uid = uid
        self.level = level

class Block(Element): 
    def __init__(self, content, parent_document, parent_container, distance=0.0):
        super().__init__()
        self.parent_container = parent_container
        self.parent_document_uid = parent_document.uid
        self.parent_container_uid = parent_container.uid
        self.content = content
        self.level = parent_container.level
        self.distance = distance
     
    def get_content(self):
        return self.content
    
    def to_dict(self):
        return {
            'uid': self.uid,
            'parent_document_uid': self.parent_document_uid,
            'parent_container_uid': self.parent_container_uid,
            'level': self.level
        }
    
    @classmethod
    def from_metadata(cls, text_content, metadata, meta_distance):
        return cls(
            content=text_content,
            parent_document=UIDWrapper(metadata.get('parent_document_uid')),
            parent_container=UIDWrapper(metadata.get('parent_container_uid'), metadata.get('level')),
            distance=meta_distance
        )


