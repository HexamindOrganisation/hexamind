import uuid
from hxm_rag.model.model.container import Container

class Document:
    def __init__(self, document_structure: dict):
        self.uid = str(uuid.uuid4())
        self.root_container = Container.from_dict(document_structure, self, None)
    
    def prepare_for_ingestion(self):
        self.root_container.get_content()