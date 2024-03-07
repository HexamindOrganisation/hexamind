from abc import ABC, abstractmethod

class ILlmClient(ABC):
    
    @abstractmethod
    def chat(self, model, message, temperature=0):
        pass

    @abstractmethod
    def create_chat_message(self, role :str, content:str):
        pass