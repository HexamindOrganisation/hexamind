from abc import ABC, abstractmethod

from hxm_rag.model.model.block import Block



class IDbClient(ABC):
    """
    Abstract class for database client
    """

    @abstractmethod
    def add_document(self, document, embedding, block: Block):
        pass

    @abstractmethod
    def get_document(self, document_id):
        pass

    @abstractmethod
    def delete_document(self, document_id):
        pass

    @abstractmethod
    def update_document(self, document, embedding, block: Block):
        pass

    @abstractmethod
    def search(self, query, num_results=10):
        pass