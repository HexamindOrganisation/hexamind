import uuid
from hxm_rag.model.modelv2.container import Container
from hxm_rag.model.readersv2.WordReader import WordReader
from hxm_rag.model.readersv2.HtmlReader import HtmlReader

class Document:
    def __init__(self, path):
        self.path = path
        self.uid = str(uuid.uuid4())
        self.root_container_dict = HtmlReader(path).document_structure
        self.root_container = Container.from_dict(self.root_container_dict, self)
    
    def prepare_for_ingestion(self):
        self.root_container.get_content()