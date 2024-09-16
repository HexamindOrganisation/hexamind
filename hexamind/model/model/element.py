from typing import List, Optional, Union, Dict, Any
import uuid
from abc import ABC, abstractmethod


class Element(ABC):
    def __init__(
        self,
        parent_uid: Optional[str],
        title: str,
        level: int,
        section_number: str,
        metadatas: Optional[List[Dict[str, Any]]] = [],
    ) -> None:
        self.uid: str = str(uuid.uuid4())
        self.parent_uid: Optional[str] = parent_uid
        self.title: str = title
        self.level: int = level
        self.section_number: str = section_number
        self.metadatas: List[Dict[str, Any]] = metadatas

    @abstractmethod
    def get_content(self) -> str:
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass
