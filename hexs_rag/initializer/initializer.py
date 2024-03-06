import os
import logging.config
import chromadb 
from dotenv import load_dotenv

load_dotenv()

DATABASE_PATH = os.getenv('DATABASE_PATH')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')


class Initializer:
    def __init__(self): # config
        # TODO config assigned ENV variables, non sure if necessary as we directly access from env
        pass
        # self.config = config

    #TODO Logs at later point
    # def initialize_logging(self):
    #     """Initializes logging configuration."""
    #     logging.config.fileConfig(self.config.logging_config_file_path)

    def initialize_database(self):
        """Initializes and returns the database and collection."""
        if not os.path.exists(DATABASE_PATH): 
            os.makedirs(DATABASE_PATH) 
        client_db = chromadb.PersistentClient(DATABASE_PATH) # TODO generalize to all dbs?
        collection = client_db.get_or_create_collection(COLLECTION_NAME)
        return client_db, collection



