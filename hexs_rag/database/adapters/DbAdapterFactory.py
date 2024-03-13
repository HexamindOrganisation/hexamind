from hexs_rag.database.adapters.ChromaDbAdapter import ChromaDbAdapter
from hexs_rag.database.adapters.MilvusDbAdapter import MilvusDbAdapter
import os
import chromadb

class DbAdapterFactory:
    """
    Factory class for creating the database adapter
    """

    @staticmethod
    def create_adapter(db_name, collection_name = None, **kwargs):
        """
        Create the proper adapter for the database according to the configuration.
        """

        database_path = database_path if database_path is not None else os.getenv('DATABASE_PATH')
        collection_name = collection_name if collection_name is not None else os.getenv('COLLECTION_NAME', 'default')

        if db_name == 'chroma':
            try:
                if kwargs['database_path']:
                    database_path = kwargs['database_path']
                else: 
                    raise ValueError('Missing environment variable for database path.')
                
                return ChromaDbAdapter(chromadb.PersistentClient(database_path), collection_name)
            except Exception as e:
                raise ValueError(f"Could not create ChromaDbAdapter: {e}")
            
        elif db_name == 'milvus':
            try:
                return MilvusDbAdapter(collection_name=collection_name, **kwargs)
            except Exception as e:
                raise ValueError(f"Could not create MilvusDbAdapter: {e}")
        else:
            raise ValueError(f"Unsupported database name: {db_name}")
 