from .AbstractDb import IDbClient


class ChromaDbAdapter(IDbClient):
    def __init__(self, client, collection_name):
        self.client = client
        self.collection = self.client.get_or_create_collection(collection_name)

    def add_document(self, document, embedding, block):
        self.collection.add(
            documents=[document],
            embeddings=[embedding],
            ids=[block.index],
            metadatas=[block.to_dict()],
        )

    def get_document(self, document_id):
        self.collection.get(ids=[document_id])

    def delete_document(self, document_id):
        self.collection.delete(ids=[document_id])

    def update_document(self, document, embedding, block):
        self.collection.update(
            documents=[document],
            embeddings=[embedding],
            ids=[block.index],
            metadatas=[block.to_dict()],
        )

    def search(self, query, num_results=10):
        # TODO implement search
        pass
