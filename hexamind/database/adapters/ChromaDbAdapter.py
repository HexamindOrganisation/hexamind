import logging
from .AbstractDb import IDbClient
from hexamind.model.chunk.chunk import Chunk

logger = logging.getLogger(__name__)


class ChromaDbAdapter(IDbClient):
    def __init__(self, client, collection_name):
        self.client = client
        self.collection = self.client.get_or_create_collection(collection_name)

    def add_document(self, document, embedding, ids, metadatas):
        self.collection.add(
            documents=[document],
            embeddings=[embedding],
            ids=[ids],
            metadatas=[metadatas],
        )

    def get_document(self, document_id):
        return self.collection.get(ids=[document_id])

    def delete_document(self, document_id):
        self.collection.delete(ids=[document_id])

    def update_document(self, document, embedding, ids, metadatas):
        self.collection.update(
            documents=[document],
            embeddings=[embedding],
            ids=[ids],
            metadatas=[metadatas],
        )

    def get(self):
        return self.collection.get(include=["embeddings", "documents", "metadatas"])

    def search(self, query, num_results=10, condition=None):
        condition = self._translate_condition(condition)
        results = self.collection.query(
            query_embeddings=query, n_results=num_results, where=condition
        )
        logger.debug(f"Search query results:\n{results}")
        contents = results["documents"][0]
        metadatas = results["metadatas"][0]

        chunks = []
        for content, metadata in zip(contents, metadatas):
            chunk = Chunk(
                content,
                metadata["container_uid"],
                metadata["document_uid"],
                metadata["title"],
                metadata["level"],
                metadata["document_title"],
                metadata["section_number"],
                metadata["index"],
                metadata["distance"],
            )
            chunks.append(chunk)

        return chunks

    def _translate_condition(self, condition=None):
        if condition is None:
            return None

        return condition

    def hybrid_search(
        self, query_dense_vector, query_sparse_vector, num_results=10, condition=None
    ):
        pass
