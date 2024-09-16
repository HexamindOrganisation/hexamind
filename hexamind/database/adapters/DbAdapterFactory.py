import os

import chromadb

from hexamind.database.adapters.ChromaDbAdapter import ChromaDbAdapter
from hexamind.database.adapters.ElasticSearchAdapter import ElasticSearchAdapter


class DbAdapterFactory:
    """
    Factory class for creating the database adapter
    """

    @staticmethod
    def create_adapter(db_name, collection_name=None, **kwargs):
        """
        Create the proper adapter for the database according to the configuration.
        """
        database_path = kwargs.get("database_path") or os.getenv("DATABASE_PATH")
        if not database_path:
            raise ValueError("Missing environment variable for database path.")

        collection_name = collection_name or os.getenv("COLLECTION_NAME", "default")

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
