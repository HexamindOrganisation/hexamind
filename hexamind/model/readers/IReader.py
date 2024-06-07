from abc import ABC, abstractmethod
from hexamind.model.transformer.MkTransformer import MkTransformer
class IReader(ABC):

    @abstractmethod
    def _convert_to_markdown(self) -> str:
        pass

    @abstractmethod
    def read(self):
        return MkTransformer.from_markdown(self._convert_to_markdown())