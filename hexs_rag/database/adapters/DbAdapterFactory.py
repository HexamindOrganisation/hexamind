from hexs_rag.database.adapters.ChromaDbAdapter import ChromaDbAdapter
import os
from chromadb import PersistentClient 

class DbAdapterFactory:
    """
    Factory class for creating the database adapter
    """

    @staticmethod
    def create_adapter(db_name, database_path = None, collection_name = None):
        """
        Create the proper adapter for the database according to the configuration.
        """

        database_path = database_path if database_path is not None else os.getenv('DATABASE_PATH')
        collection_name = collection_name if collection_name is not None else os.getenv('COLLECTION_NAME', 'default')

        if not database_path:
            raise ValueError('Missing environment variable for database path.')
        
        if db_name == 'chroma':
            try:
                return ChromaDbAdapter(PersistentClient(database_path), collection_name)
            except Exception as e:
                raise ValueError(f"Could not create ChromaDbAdapter: {e}")
        else:
            raise ValueError(f"Unsupported database name: {db_name}")
 