import logging
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct, NamedVector
from qdrant_client.http.models import Filter, FieldCondition, MatchValue, FilterSelector
from .AbstractDb import IDbClient
from hexamind.model.chunk.chunk import Chunk
import os

logger = logging.getLogger(__name__)


class QdrantDbAdapter(IDbClient):
    def __init__(
        self,
        url=os.getenv("QDRANT_URL"),
        collection_name="qdrant_collection",
        dense_dim=1024,
        sparse_dim=30522,
    ):
        self.collection_name = collection_name
        self.dense_dim = dense_dim
        self.sparse_dim = sparse_dim
        self.client = QdrantClient(url=url)
        logger.info(f"QdrantDbAdapter initialized with collection: {collection_name}")

    def get_collections(self):
        collections = self.client.get_collections()
        logger.debug(f"Retrieved {len(collections.collections)} collections")
        return collections

    def create_collection(self):
        logger.info(f"Creating collection: {self.collection_name}")
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config={
                "sparse": VectorParams(size=self.sparse_dim, distance=Distance.COSINE),
                "dense": VectorParams(size=self.dense_dim, distance=Distance.COSINE),
            },
        )
        logger.info(f"Collection {self.collection_name} created successfully")

    def add_document(self, document, dense_embedding, sparse_embedding, ids, metadatas):
        logger.info(f"Adding document with id: {ids}")
        points = [
            PointStruct(
                id=ids,
                vector={"sparse": sparse_embedding, "dense": dense_embedding},
                payload={"document": document, "metadata": metadatas},
            )
        ]
        self.client.upsert(collection_name=self.collection_name, points=points)
        logger.debug(f"Document added successfully: {ids}")

    def get_document(self, document_id):
        logger.info(f"Retrieving document with id: {document_id}")
        result = self.client.retrieve(
            collection_name=self.collection_name, ids=[document_id]
        )
        if result:
            logger.debug(f"Document retrieved: {document_id}")
            return result[0]
        logger.warning(f"Document not found: {document_id}")
        return None

    def delete_document(self, document_id):
        logger.info(f"Deleting document with id: {document_id}")
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=FilterSelector(
                filter=Filter(
                    must=[
                        FieldCondition(
                            key="metadata.document_uid",
                            match=MatchValue(value=document_id),
                        )
                    ]
                )
            ),
        )
        logger.debug(f"Document deleted: {document_id}")

    def update_document(self, document, embedding, ids, metadatas):
        logger.info(f"Updating document with id: {ids}")
        self.add_document(document, embedding, ids, metadatas)
        logger.debug(f"Document updated: {ids}")

    def get(self):
        logger.info("Retrieving all points")
        scroll_result = self.client.scroll(
            collection_name=self.collection_name, limit=100
        )
        logger.debug(f"Retrieved {len(scroll_result['points'])} points")
        return scroll_result["points"]

    def _translate_condition(self, condition=None):
        if condition is None:
            return None

        logger.debug(f"Translating condition: {condition}")
        should_conditions = []
        for field, criteria in condition.items():
            for operator, value in criteria.items():
                if operator == "$in":
                    for v in value:
                        should_conditions.append(
                            FieldCondition(
                                key=f"metadata.{field}", match=MatchValue(value=v)
                            )
                        )

        logger.debug(f"Translated condition: {should_conditions}")
        return Filter(should=should_conditions)

    def search(self, query_vector, vector_name, num_results=10, condition=None):
        logger.info(
            f"Performing search with vector_name: {vector_name}, num_results: {num_results}"
        )
        condition = self._translate_condition(condition)
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=NamedVector(name=vector_name, vector=query_vector),
            limit=num_results,
            query_filter=condition,
            with_payload=True,
        )

        chunks = []
        for result in search_result:
            dict_chunk = result.payload["metadata"]
            chunk = Chunk(**dict_chunk)
            chunk.id = result.id
            chunk.distance = result.score
            chunks.append(chunk)

        logger.debug(f"Search returned {len(chunks)} chunks")
        return chunks

    def hybrid_search(
        self, query_dense_vector, query_sparse_vector, num_results=10, condition=None
    ):
        logger.warning(
            "The hybrid_search method in QdrantDbAdapter is deprecated. Use the Retriever class for hybrid search."
        )
        return []
