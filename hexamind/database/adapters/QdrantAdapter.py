from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct, CollectionStatus, SearchRequest, NamedVector, NamedSparseVector
from qdrant_client.http.models import Filter, FieldCondition, MatchValue, FilterSelector
from .AbstractDb import IDbClient
from hexamind.model.chunk.chunk import Chunk
from concurrent.futures import ThreadPoolExecutor, as_completed
import ranx
import os
import logging
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QdrantDbAdapter(IDbClient):
    def __init__(self, url = os.getenv("QDRANT_URL"), collection_name="qdrant_collection", dense_dim=1024, sparse_dim=30522):
        self.collection_name = collection_name
        self.dense_dim = dense_dim
        self.sparse_dim = sparse_dim
        # Connect to Qdrant
        self.client = QdrantClient(url=url)

        # Check if the collection exists, if not, create it
    
    def get_collections(self):
        return self.client.get_collections()
    
    def create_collection(self):
          self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config={
                    "sparse": VectorParams(size=self.sparse_dim, distance=Distance.COSINE),
                    "dense" :VectorParams(size=self.dense_dim, distance=Distance.COSINE)}

            )

    def add_document(self, document, dense_embedding, sparse_embedding, ids, metadatas):
        points = [
            PointStruct(
                id=ids,
                vector={"sparse": sparse_embedding, "dense": dense_embedding},
                payload={
                    "document": document,
                    "metadata": metadatas
                }
            )
        ]
        self.client.upsert(collection_name=self.collection_name, points=points)

    def get_document(self, document_id):
        result = self.client.retrieve(collection_name=self.collection_name, ids=[document_id])
        if result:
            return result[0]
        return None

    def delete_document(self, document_id):
        self.client.delete(collection_name=self.collection_name, 
                           points_selector=FilterSelector(
                               filter=Filter(
                                      must=[
                                        FieldCondition(
                                             key="metadata.document_uid",
                                             match=MatchValue(value=document_id)
                                        )
                                      ]
                                 )
                           )

        )

    def update_document(self, document, embedding, ids, metadatas):
        self.add_document(document, embedding, ids, metadatas)

    def get(self):
        # Retrieve all points (not efficient for large collections)
        scroll_result = self.client.scroll(collection_name=self.collection_name, limit=100)
        return scroll_result["points"]

    def search(self, query_dense_vector, query_sparse_vector, num_results=10, condition=None):
        condition = self._translate_condition(condition)
        print(condition)
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector={
                NamedVector(
                    name="sparse",
                    vector=query_sparse_vector
                ),
                NamedVector(
                    name="dense",
                    vector=query_dense_vector
                )
            },
            limit=num_results,
            query_filter=condition,
            with_payload=True
        )

        return search_result

        """chunks = []
        for result in search_result:
            dict_chunk = result.payload['metadata']
            chunk = Chunk(**dict_chunk)
            chunks.append(chunk)

        return chunks """
    
    def hybrid_search(self, query_dense_vector, query_sparse_vector, num_results=10, condition=None):
        condition = self._translate_condition(condition)
        search_result = self.client.search_batch(
            collection_name=self.collection_name,
            
            requests=[
                SearchRequest(
                    vector=NamedVector(
                        name="dense",
                        vector=query_dense_vector
                    ),
                    with_payload=True,
                    filter=condition,
                    limit=num_results,
                ),
                SearchRequest(
                    vector=NamedVector(
                        name="sparse",
                        vector=query_sparse_vector
                    ),
                    with_payload=True,
                    filter=condition,
                    limit=num_results,
                ),
            ]
        )

        logger.info(f"Got result from hybrid search")

        dense_results = search_result[0]
        sparse_results = search_result[1]

        combined_results = dense_results + sparse_results

        chunks = []
        for result in combined_results:
            dict_chunk = result.payload['metadata']
            chunk = Chunk(**dict_chunk)
            chunks.append(chunk)
        
        logger.info(f"Created chunks from combined results")
        
        return chunks

    def _translate_condition(self, condition=None):
        if condition is None:
            return None
        
        should_conditions = []
        for field, criteria in condition.items():
            print(field, criteria)
            for operator, value in criteria.items():
                print(operator, value)
                if operator == "$in":
                    print(value)
                    for v in value:
                        should_conditions.append(
                            FieldCondition(
                                key=f"metadata.{field}",
                                match=MatchValue(
                                    value=v
                                )
                            )
                        )

            return Filter(should=should_conditions)