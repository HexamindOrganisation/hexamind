from abc import ABC, abstractmethod
import uuid

class Element(ABC):
    def __init__(self):
        self.uid = str(uuid.uuid4())
        self.content = ''
    
    @abstractmethod 
    def get_content(self):
        pass

    @abstractmethod
    def to_dict(self):
        pass