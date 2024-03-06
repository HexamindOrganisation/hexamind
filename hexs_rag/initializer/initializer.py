# Description: Initialization class that instantiates the database.
# TODO connector for databases



import os
import logging
from dotenv import load_dotenv
import chromadb

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
    """

    def __init__(self):
        """Loads environment variables and initializes instance attributes."""
        load_dotenv(dotenv_path=".env")
        self.database_path = os.getenv('DATABASE_PATH')
        self.collection_name = os.getenv('COLLECTION_NAME')
        if not self.database_path or not self.collection_name:
            logging.error('DATABASE_PATH or COLLECTION_NAME environment variables are not set.')
            raise ValueError('Missing environment variables for database initialization.')

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
            raise



