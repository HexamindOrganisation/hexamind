from abc import ABC, abstractmethod
from hexamind.model.builder.MkBuilder import MkBuilder
class IReader(ABC):

    @abstractmethod
    def convert_to_markdown(self) -> str:
        pass

