# Description: Initialization class that instantiates the database.
# TODO connector for databases
# TODO initialization might need a redesign for the library



import os
import logging
import chromadb
from hexs_rag.llm.llm import LlmAgent
from hexs_rag.llm.adapters import LlmAdapterFactory

# Initialize logging with a basic configuration for debugging purposes
logging.basicConfig(level=logging.INFO)

class Initializer:
    """
    Initialization class that instantiates the database using environment variables
    for configuration. This class is responsible for ensuring the database directory exists
    and obtaining a reference to a specific collection within the database.

    Attributes:
    - None currently, but utilizes environment variables:
      - DATABASE_PATH: Path to the database directory.
      - COLLECTION_NAME: Name of the collection to use or create.

    Methods:
    - initialize_database: Initializes the database and collection.
    - initialize_llm: Initializes the LLM client.

    Note: This class can be inherited to add a method for initializing your custom controller or any other initialization logic.
    """

    def __init__(self, database_path = None, collection_name = None, llm_name=None, llm_api_key=None, model=None, embed_model=None):
        """Loads environment variables and initializes instance attributes."""
        self.database_path = database_path or os.getenv('DATABASE_PATH')
        self.collection_name = collection_name or os.getenv('COLLECTION_NAME')
        if not self.database_path or not self.collection_name:
            logging.error('DATABASE_PATH or COLLECTION_NAME environment variables are not set.')
            raise ValueError('Missing environment variables for database initialization.')
        
        self.llm_name = llm_name or os.getenv('LLM_NAME')
        self.llm_api_key = llm_api_key or os.getenv('LLM_API_KEY')
        if not self.llm_api_key:
            logging.error('LLM_API_KEY variable is not set.')
            raise ValueError('Missing variable for LLM API key.')
        
        self.model = model
        self.embed_model = embed_model

    def initialize_database(self):
        """Initializes and returns the database and collection."""
        try:
            if not os.path.exists(self.database_path):
                os.makedirs(self.database_path)
                logging.info(f"Database directory created at: {self.database_path}")
            
            client_db = chromadb.PersistentClient(self.database_path)
            collection = client_db.get_or_create_collection(self.collection_name)
            return client_db, collection
        except Exception as e:
            logging.error(f"Failed to initialize the database: {e}")
            raise Exception(f"Failed to initialize the database: {e}") # TODO remove one of these later

    def initialize_llm(self) -> LlmAgent:
        """Initializes the LLM client."""
        try:
            llm_adapter = LlmAdapterFactory.create_adapter(self.llm_name, self.llm_api_key, self.model, self.embed_model)
            return LlmAgent(llm_adapter)
                
        except Exception as e:
            logging.error(f"Failed to initialize the LLM client: {e}")
            raise
