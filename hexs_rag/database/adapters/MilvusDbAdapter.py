import os

from pymilvus import (Collection, CollectionSchema, DataType, FieldSchema,
                      connections, db)

from hexs_rag.database.adapters.AbstractDb import IDbClient
from hexs_rag.model.model.block import Block

# TODO : MUST BE INTENSIVELY TESTED BECAUSE NOT SURE OF THE IMPLEMENTATION
# TODO : GET METHOD NOT IMPLEMENTED
# COULD BE DELETED LATER


class MilvusDbAdapter(IDbClient):
    def __init__(
        self,
        database_name=None,
        host=None,
        port=None,
        user=None,
        password=None,
        collection_name=None,
    ):

        self.db_name = (
            database_name
            if database_name is not None
            else os.getenv("API_DB_NAME_", "default")
        )
        self.host = host if host is not None else os.getenv("API_DB_HOST", "localhost")
        self.port = port if port is not None else os.getenv("API_DB_PORT", 19530)
        self.user = user if user is not None else os.getenv("API_DB_USER", "root")
        self.password = (
            password if password is not None else os.getenv("API_DB_PASSWORD", "")
        )
        self.collection_name = (
            collection_name
            if collection_name is not None
            else os.getenv("COLLECTION_NAME", "default")
        )

        try:
            self.client = connections.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                db_name=self.db_name,
            )

            self.collection = self._create_collection()

        except Exception as e:
            raise e

    def _create_collection(self):
        documents = FieldSchema(
            name="documents", dtype=DataType.STRING, is_primary=True, auto_id=False
        )
        embeddings = FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR)
        ids = FieldSchema(name="ids", dtype=DataType.INT64)
        metadatas = FieldSchema(name="metadatas", dtype=DataType.STRING)

        schema = CollectionSchema(
            fields=[documents, embeddings, ids, metadatas],
            primary_field="documents",
            description="RAG collection",
        )
        collection = Collection(name=self.collection_name, schema=schema)

        return collection

    def add_document(self, document, embedding, block: Block):
        self.collection.insert(
            [[document], [embedding], [block.index], [block.to_dict()]]
        )

    """
    def get_document(self, document_id):
        filter = f"ids == {document_id}"
        self.collection.get(filter
    """

    def delete_document(self, document_id):
        filter = f"ids == {document_id}"
        self.collection.delete(filter)

    def update_document(self, document, embedding, block: Block):
        self.collection.upsert(
            [[document], [embedding], [block.index], [block.to_dict()]]
        )
