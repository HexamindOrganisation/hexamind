from .block import Block
from .paragraph import Paragraph

INFINITE = 99999

class Container:
    """
    TODO: DOCSTRING
    """
    def __init__(self, 
                paragraphs: list[Paragraph], 
                title: Paragraph = None,  # TODO why is this a Paragraph type??
                level: int = 0, 
                index: list[int] = None, 
                father=None, 
                id_=0):
        
        if index is None: index = []
        self.level = level
        self.title = title
        self.paragraphs = []
        self.children = []
        self.index = index
        self.father = father

        if father is not None:
            self.id_ = int(str(1) + str(father.id_) + str(id_))
        else:
            self.id_ = int(str(1) + str(id_))

        if paragraphs:
            self.paragraphs, self.children = self.create_children(paragraphs, level, index)
        
        self.containers = [self]
        for child in self.children:
            self.containers += child.containers

        self.blocks = self.get_blocks()    

    @property
    def structure(self):
        self_structure = {str(self.id_): {
            'index': str(self.id_),
            'canMove': True,
            'isFolder': True,
            'children': [p.id_ for p in self.paragraphs] + [child.id_ for child in self.children],
            'canRename': True,
            'data': {},
            'level': self.level,
            'rank': self.index,
            'title': self.title.text if self.title else 'root'
        }}
        paragraphs_structure = [p.structure for p in self.paragraphs]
        structure = [self_structure] + paragraphs_structure
        for child in self.children:
            structure += child.structure
        return structure
    
    @property
    def text(self):
        text = ""
        if self.title:
            text = "Titre " + str(self.level) + " : " + self.title.text + '\n'
        for p in self.paragraphs:
                text += p.text + '\n'
        for child in self.children:
                text += child.text
        return text
    
    def get_blocks(self):
        block = Block(level=self.level, index=self.index)
        if self.title:
            self.title.text = self.title.text.replace('\r', '').replace('\n', '')
            block.title = self.title.text
            block.content = self.title.text + '/'
        temp_father = self.father
        while temp_father and type(temp_father) == Container:
            if temp_father.title:
                temp_father.title.text = temp_father.title.text.replace('\r', '').replace('\n', '')
                block.content = temp_father.title.text + '/' + block.content
            temp_father = temp_father.father
        block.content += " :\n\n"
        i = 0
        for p in self.paragraphs:
            if not p.blank:
                i = 1
                block.content += p.text
        if i == 0:
            blocks = []
        else:
            blocks = [block]
        for child in self.children:
            blocks += child.blocks
        return blocks

    def create_children(self, paragraphs, level, rank) -> ([],[]):
        """
        creates children containers or directly attached content
        and returns the list of containers and contents of level+1
        :return:
        [Content or Container]
        """
        attached_paragraphs = []
        container_paragraphs = []
        container_title = None
        children = []
        in_children = False
        level = INFINITE
        child_id = 0

        while paragraphs:
            p = paragraphs.pop(0)
            if not in_children and not p.is_structure:
                attached_paragraphs.append(p)
            else:
                in_children = True
                if p.blank:
                    continue
                if p.is_structure and p.level <= level:  # if p is higher or equal in hierarchy
                    if container_paragraphs or container_title:
                        children.append(Container(container_paragraphs, container_title, level, rank, self, child_id))
                        child_id += 1
                    container_paragraphs = []
                    container_title = p
                    level = p.level

                else:  # p is strictly lower in hierarchy
                    container_paragraphs.append(p)

        if container_paragraphs or container_title:
            children.append(Container(container_paragraphs, container_title, level, rank, self, child_id))
            child_id += 1

        return attached_paragraphs, children
    
