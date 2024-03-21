from hxm_rag.model.modelv2.element import Element
from hxm_rag.model.modelv2.block import Block

class Container(Element):
    def __init__(self, parent_document, parent_container = None, level=0):
        super().__init__()
        self.parent_container = parent_container
        self.parent_document = parent_document
        self.parent_document_uid = parent_document.uid if parent_document else None
        self.parent_container_uid = parent_container.uid if parent_container else None
        self.children = [] # adjency list
        self.level = level
    
    def get_content(self):
        content = ''
        for child in self.children:
            if isinstance(child, Block):
                content += child.content + '\n'
            elif isinstance(child, Container):
                child.get_content()
    
    def print_structure(self, indent=0): #DFS traversal to print the structure of the container
        if self.level == 0:
            print(f'Root container : {self.uid}, Level : {self.level}')
        else:
            print('  '*indent + f'Container : {self.uid}, Level : {self.level}')

        for child in self.children:
            if isinstance(child, Container):
                child.print_structure(indent+1)
            elif isinstance(child, Block):
                print('  '*(indent+1) + f'Block : {child.uid}, Level : {child.level}')
    
    def add_child(self, child):
        if isinstance(child, Container):
            child.level = self.level + 1
        self.children.append(child)
    
    @classmethod
    def from_dict(cls, structure_dict, parent_document=None, parent_container = None):
        root_container = cls(parent_document, parent_container, structure_dict.get('level', 0))

        for child in structure_dict.get('children', []):
            if child['type'] == 'container':
                child_container = cls.from_dict(child, parent_document, root_container)
                root_container.add_child(child_container)
            elif child['type'] == 'block':
                block = Block(child.get('content', ''), parent_document, root_container)
                root_container.add_child(block)
        
        return root_container