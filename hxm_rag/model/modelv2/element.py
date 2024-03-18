from abc import ABC, abstractmethod
import uuid

class Element(ABC):
    def __init__(self):
        self.uid = uuid.uuid4()
    
    @abstractmethod
    def get_content(self):
        pass