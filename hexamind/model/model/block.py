from typing import List, Optional, Union, Dict, Any
from hexamind.model.model.element import Element


class Block(Element):
    def __init__(
        self,
        parent_uid: Optional[str],
        title: str,
        level: int,
        section_number: str,
        content: str,
        metadatas: Optional[List[Dict[str, Any]]] = [],
    ):
        super().__init__(parent_uid, title, level, section_number, metadatas)
        self.content: str = content
        self.parent: Optional["Container"] = None

    def get_content(self) -> str:
        """Returns the content of the block."""
        return self.content

    def to_dict(self) -> Dict[str, Any]:
        return {
            "uid": self.uid,
            "parent_uid": self.parent_uid,
            "title": self.title,
            "level": self.level,
            "section_number": self.section_number,
            "content": self.content,
        }
