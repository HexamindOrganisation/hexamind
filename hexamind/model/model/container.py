from typing import List, Optional, Union, Dict, Any
from hexamind.model.model.element import Element
from hexamind.model.model.block import Block
from graphviz import Digraph
import platform
import os
import logging

logger = logging.getLogger(__name__)


class Container(Element):
    def __init__(
        self,
        parent_uid: Optional[str],
        title: str,
        level: int,
        section_number: str,
        metadatas: Optional[List[Dict[str, Any]]] = [],
    ):
        super().__init__(parent_uid, title, level, section_number, metadatas)
        self.children: List[Union["Container", "Block"]] = []
        self.parent: Optional["Container"] = None
        self.content: str = ""

    def add_child(self, child: Union["Container", "Block"]) -> None:
        """Adds a child to the container."""
        child.parent = self
        self.children.append(child)
        self._update_content_upwards()

    def _is_leaf_container(self) -> bool:
        """Returns True if the container is a leaf container."""
        return all(isinstance(child, Block) for child in self.children)

    def _update_content(self) -> None:
        """Updates the content of the container."""
        content_parts = []
        if not self._is_leaf_container() and self.title and self.level != 0:
            content_parts.append(f"{'#' * self.level} {self.title}")

        for child in self.children:
            content_parts.append(child.get_content())

        self.content = "\n\n".join(content_parts).strip()

    def _update_content_upwards(self) -> None:
        """Updates the content of the container and its parents."""
        self._update_content()
        if self.parent:
            self.parent._update_content_upwards()

    def get_content(self) -> str:
        """Returns the content of the container."""
        return self.content

    def _get_structure_string(self, prefix: str = "", is_last: bool = True) -> str:
        """Returns the structure of the container."""
        structure_str = ""
        if (self.level) == 0 and (self.parent is None) and (self.parent_uid is None):
            structure_str += "Root container, Level: 0\n"
        else:
            connector = "└── " if is_last else "├── "
            structure_str += f"{prefix}{connector}Container, Level: {self.level}, Section number: {self.section_number}\n"
            prefix += "    " if is_last else "│   "

        child_count = len(self.children)
        for i, child in enumerate(self.children):
            is_last_child = i == child_count - 1
            if isinstance(child, Container):
                structure_str += child._get_structure_string(prefix, is_last_child)
            elif isinstance(child, Block):
                connector = "└── " if is_last_child else "├── "
                structure_str += f"{prefix}{connector}Block, Level: {child.level}, Section number: {self.section_number}\n"

        return structure_str

    def __add_to_graph(self, dot, parent_id=None) -> None:
        node_id = self.uid
        label = (
            f"Container\nLevel: {self.level}" if self.level != 0 else "Root\nContainer"
        )
        dot.node(node_id, label)

        if parent_id:
            dot.edge(parent_id, node_id)

        for child in self.children:
            if isinstance(child, Container):
                child.__add_to_graph(dot, node_id)
            elif isinstance(child, Block):
                child_id = child.uid
                dot.node(child_id, f"Block\nLevel: {child.level}")
                dot.edge(node_id, child_id)

    def visualize(self, filename="container_structure") -> None:
        dot = Digraph(comment="Container Structure")
        self.__add_to_graph(dot)
        rendered_path = dot.render(filename, format="pdf", view=True)

        current_os = platform.system()

        try:
            if current_os == "Windows":
                os.startfile(rendered_path)
            elif current_os == "Darwin":
                os.system(f"open {rendered_path}")
            elif current_os == "Linux":
                os.system(f"xdg-open {rendered_path}")
        except Exception as e:
            logger.error(f"Error opening the rendered graph: {e}")
            logger.info("Please open the file manually")

    def __str__(self) -> str:
        return self._get_structure_string()

    def __getitem__(self, index: int) -> Union["Container", "Block"]:
        sliced_container = Container(
            self.parent_uid, self.title, self.level, self.section_number
        )
        sliced_container.children = self.children[index]
        return sliced_container

    def to_dict(self) -> Dict[str, Any]:
        return {
            "uid": self.uid,
            "parent_uid": self.parent_uid,
            "title": self.title,
            "level": self.level,
            "section_number": self.section_number,
            "content": self.content,
            "children": [child.to_dict() for child in self.children],
        }
