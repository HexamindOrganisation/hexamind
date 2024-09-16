from abc import ABC, abstractmethod
from typing import List


class ITokenizer(ABC):
    @abstractmethod
    def tokenize(self, text: str) -> List[str]:
        pass

    @abstractmethod
    def decode(self, tokens: List[str]) -> str:
        pass

    @abstractmethod
    def count_tokens(self, text: str) -> int:
        pass
