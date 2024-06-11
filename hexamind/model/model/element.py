from typing import List, Optional, Union
import uuid
from abc import ABC, abstractmethod

class Element(ABC): 
    def __init__(self, parent_uid: Optional[str], title: str, level: int, section_number: str):
        self.uid: str = str(uuid.uuid4())
        self.parent_uid: Optional[str] = parent_uid
        self.title: str = title
        self.level: int = level
        self.section_number: str = section_number
    
    @abstractmethod
    def get_content(self) -> str:
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass
    