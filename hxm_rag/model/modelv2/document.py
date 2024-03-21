import uuid
from hxm_rag.model.modelv2.container import Container
from hxm_rag.model.readersv2.PdfReader import PdfReader

class Document:
    def __init__(self, path):
        self.path = path
        self.uid = uuid.uuid4()
        self.root_container_dict = PdfReader(self.path).root_container
        self.root_container = Container.from_dict(self.root_container_dict, self)