import os

import chromadb

from hxm_rag.database.adapters.ChromaDbAdapter import ChromaDbAdapter
from hxm_rag.database.adapters.ElasticSearchAdapter import \
    ElasticSearchAdapter


class DbAdapterFactory:
    """
    Factory class for creating the database adapter
    """

    @staticmethod
    def create_adapter(db_name, collection_name=None, **kwargs):
        """
        Create the proper adapter for the database according to the configuration.
        """
        if kwargs["database_path"]:
            database_path = kwargs["database_path"]
        else:
            raise ValueError("Missing environment variable for database path.")
            
        database_path = (
            database_path if database_path is not None else os.getenv("DATABASE_PATH")
        )
        
        collection_name = (
            collection_name
            if collection_name is not None
            else os.getenv("COLLECTION_NAME", "default")
        )

        if db_name == "chroma":
            try:
  

                return ChromaDbAdapter(
                    chromadb.PersistentClient(database_path), collection_name
                )
            except Exception as e:
                raise ValueError(f"Could not create ChromaDbAdapter: {e}")

        elif db_name == "elasticsearch":
            try:
                return ElasticSearchAdapter(**kwargs)
            except Exception as e:
                raise ValueError(f"Could not create ElasticSearchAdapter: {e}")
        else:
            raise ValueError(f"Unsupported database name: {db_name}")