import uuid
from hxm_rag.model.modelv2.container import Container
from hxm_rag.model.readersv2.PdfReader import PdfReader
from hxm_rag.model.readersv2.WordReader import WordReader

class Document:
    def __init__(self, path):
        self.path = path
        self.uid = uuid.uuid4()
        self.root_container_dict = WordReader(path).document_structure
        self.root_container = Container.from_dict(self.root_container_dict, self)