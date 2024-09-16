from abc import ABC, abstractmethod

from hexamind.model.model.block import Block
from hexamind.model.chunk.chunk import Chunk
from typing import List


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
    def search(self, query, num_results=10) -> List[Chunk]:
        pass

    @abstractmethod
    def _translate_condition(self, condition=None):
        pass

    def hybrid_search(
        self, query_dense_vector, query_sparse_vector, num_results=10, condition=None
    ):
        pass
