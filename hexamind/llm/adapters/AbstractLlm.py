from abc import ABC, abstractmethod


class ILlmClient(ABC):
    """
    Interface for the LLM client.
    This is an abstract class that defines the methods that should be implemented by the LLM client.
    It allows to generalize the use of different LLMs using APIs.
    """

    @abstractmethod
    def chat(self, messages, temperature=0):
        pass

    @abstractmethod
    def create_chat_message(self, role: str, content: str):
        pass

    @abstractmethod
    def embeddings(self, input):
        pass
