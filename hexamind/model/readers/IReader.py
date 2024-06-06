from abc import ABC, abstractmethod

class IReader(ABC):

    @abstractmethod
    def convert_to_markdown(self) -> str:
        pass