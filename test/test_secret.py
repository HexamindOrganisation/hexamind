# Description: use this testing suite to test if secret variables are working correctly

import os
import unittest
from hxm_rag.initializer.initializer import Initializer

class MyApiTests(unittest.TestCase):
    def test_something_with_api(self):
        api_key = os.environ['LLM_API_KEY']

        battery = Initializer( # initializes instance attributes
        database_path = './database_test', 
        db_name = 'chroma', # chroma db name
        collection_name = 'test_collection', 
        llm_name = "mistral", # either mistral or openai 
        llm_api_key = api_key
        )
        assert battery is not None
        db_adapter = battery.initialize_database() # Initializes and returns the database and collection
        assert db_adapter is not None