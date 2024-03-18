from hxm_rag.model.modelv2.element import Element
from hxm_rag.model.modelv2.block import Block

class Container(Element):
    def __init__(self, parent_document, parent_container = None, level=0):
        super().__init__()
        self.parent_document_uid = parent_document.uid
        self.parent_container_uid = parent_container.uid if parent_container else None
        self.children = [] # adjency list
        self.level = level
    
    def get_content(self):
        return ' '.join(child.get_content() for child in self.children if isinstance(child, Block))
    
    def print_structure(self, indent=0): #DFS traversal to print the structure of the container
        if self.level == 0:
            print(f'Root container : {self.uid}, Level : {self.level}')
        else:
            print('  '*indent + f'Container : {self.uid}, Level : {self.level}')

        for child in self.children:
            if isinstance(child, Container):
                child.print_structure(indent+1)
            elif isinstance(child, Block):
                print('  '*(indent+1) + f'Block : {child.uid}, Level : {child.level}, Content : {child.get_content()}')
    
    def add_child(self, child):
        if isinstance(child, Container):
            child.level = self.level + 1
        self.children.append(child)