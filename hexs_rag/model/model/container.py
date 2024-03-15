from typing import List, Optional
from .block import Block
from .paragraph import Paragraph

INFINITE = 99999


class Container:
    """
    A class to represent a container for paragraphs and other containers.
    
    Attributes:
        level (int): The hierarchy level of the container.
        title (Optional[Paragraph]): The title of the container as a paragraph, if any.
        paragraphs (List[Paragraph]): The list of paragraphs contained directly within this container.
        children (List[Container]): The list of child containers contained within this container.
        index (List[int]): The hierarchical index representing the position of this container.
        father (Optional[Container]): The parent container of this container.
        id_ (int): A unique identifier for the container.
        containers (List[Container]): A list of this container along with all its descendant containers.
        blocks (List[Block]): A list of block representations of the container's content.
    
    Methods:
        structure: Returns a structure representation of the container and its content.
        text: Returns the textual representation of the container's title and paragraphs.
        get_blocks: Generates block objects for the container's content.
        create_children: Splits paragraphs into attached and container paragraphs, creating child containers as necessary.
    """

    def __init__(
        self,
        paragraphs: List[Paragraph],
        title: Optional[Paragraph] = None,
        level: int = 0,
        index: Optional[List[int]] = None,
        father: Optional["Container"] = None,
        id_: int = 0,
    ) -> None:
        self.level = level
        self.title = title
        self.paragraphs: List[Paragraph] = []
        self.children: List[Container] = []
        self.index = index if index is not None else []
        self.father = father
        self.id_ = int(f"1{father.id_ if father else ''}{id_}")

        if paragraphs:
            self.paragraphs, self.children = self.create_children(
                paragraphs, level, self.index
            )

        self.containers: List[Container] = [self] + [
            child for child in self.children for container in child.containers
        ]

        self.blocks = self.get_blocks()

    @property
    def structure(self) -> dict:
        self_structure = {
            str(self.id_): {
                "index": str(self.id_),
                "canMove": True,
                "isFolder": True,
                "children": [p.id_ for p in self.paragraphs]
                + [child.id_ for child in self.children],
                "canRename": True,
                "data": {},
                "level": self.level,
                "rank": self.index,
                "title": self.title.text if self.title else "root",
            }
        }
        paragraphs_structure = [p.structure for p in self.paragraphs]
        structure = [self_structure] + paragraphs_structure
        for child in self.children:
            structure += child.structure
        return structure

    @property
    def text(self) -> str:
        text = f"Title {self.level}: {self.title.text}\n" if self.title else ""
        for paragraph in self.paragraphs:
            text += f"{paragraph.text}\n"
        for child in self.children:
            text += child.text
        return text

    def _prepare_title_text(self, title: Paragraph) -> str:
        """Cleans the title text by removing carriage returns and newlines."""
        return title.text.replace("\r", "").replace("\n", "")

    def _accumulate_ancestor_titles(self, initial_content: str) -> str:
        """Accumulates titles from ancestor containers, appending them to the initial content."""
        content = initial_content
        ancestor = self.father
        while ancestor and isinstance(ancestor, Container):
            if ancestor.title:
                content = f"{self._prepare_title_text(ancestor.title)}/{content}"
            ancestor = ancestor.father
        return content

    def get_blocks(self) -> List[Block]:  # this isn't the same method as the one in Doc
        """Generates block objects for the container's content, including handling of titles."""
        block = Block(level=self.level, index=self.index)
        if self.title:
            cleaned_title = self._prepare_title_text(self.title)
            block.title = cleaned_title
            block.content = f"{cleaned_title}/"
        block.content = self._accumulate_ancestor_titles(block.content) + " :\n\n"
        block_filled = any(not paragraph.blank for paragraph in self.paragraphs)
        blocks = [block] if block_filled else []
        for child in self.children:
            blocks.extend(child.get_blocks())
        return blocks

    def _classify_paragraphs(
        self, paragraphs: List[Paragraph]
    ) -> (List[Paragraph], List[Paragraph], bool, int):
        """Classifies paragraphs into those to be attached directly and those to be contained, tracking hierarchy changes."""
        attached_paragraphs = []
        container_paragraphs = []
        in_children = False
        current_level = INFINITE
        for paragraph in paragraphs:
            if not in_children and not paragraph.is_structure:
                attached_paragraphs.append(paragraph)
            else:
                in_children = True
                if paragraph.blank:
                    continue
                if paragraph.is_structure and paragraph.level <= current_level:
                    return (
                        attached_paragraphs,
                        container_paragraphs,
                        True,
                        paragraph.level,
                    )
                else:
                    container_paragraphs.append(paragraph)
        return attached_paragraphs, container_paragraphs, in_children, current_level

    def _create_child_container(
        self,
        paragraphs: List[Paragraph],
        title: Optional[Paragraph],
        level: int,
        rank: List[int],
        child_id: int,
    ):
        """Creates a child container with given paragraphs, title, and hierarchy information."""
        return Container(paragraphs, title, level, rank, self, child_id)

    def create_children(self, paragraphs: List[Paragraph], level: int, rank: List[int]):
        """Splits paragraphs into attached and container paragraphs, creating child containers as necessary."""
        children = []
        child_id = 0
        while paragraphs:
            (
                attached_paragraphs,
                container_paragraphs,
                in_children,
                current_level,
            ) = self._classify_paragraphs(paragraphs)
            if container_paragraphs or self.title:
                children.append(
                    self._create_child_container(
                        container_paragraphs, self.title, current_level, rank, child_id
                    )
                )
                child_id += 1
            paragraphs = paragraphs[
                len(attached_paragraphs) + len(container_paragraphs) :
            ]
        return attached_paragraphs, children
