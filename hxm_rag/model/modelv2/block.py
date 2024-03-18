from hxm_rag.model.modelv2.element import Element

class Block(Element):
    def __init__(self, content, parent_document, parent_container):
        super().__init__()
        self.parent_container = parent_container
        self.parent_document_uid = parent_document.uid
        self.parent_container_uid = parent_container.uid
        self.content = content
        self.level = parent_container.level
    
    def get_content(self):
        return self.content
