import os 
import pytest

from hxm_rag.initializer.initializer import Initializer
from hxm_rag.database.ingestion.ingestor import Ingestor
from hxm_rag.llm.llm.LlmAgent import LlmAgent
from hxm_rag.retriever.retriever import Retriever
from hxm_rag.model.model.doc import Doc 

@pytest.fixture
def battery_setup():
    api_key = os.environ['LLM_API_KEY']
    battery = Initializer(
        database_path='./database_test',
        db_name='chroma',
        collection_name='test_collection',
        llm_name="mistral",
        llm_api_key=api_key
    )
    return battery

@pytest.fixture
def db_adapter_setup(battery_setup):
    db_adapter = battery_setup.initialize_database() # Initializes and returns the database and collection
    return db_adapter

@pytest.fixture
def llm_agent_setup(battery_setup):
    llm_agent = battery_setup.initialize_llm()
    return llm_agent