# Description: setup for integration tests
import os 
import pytest
import shutil

from hxm_rag.initializer.initializer import Initializer
# TODO add additional teardown if required

@pytest.fixture
def battery_setup():
    api_key = os.environ['LLM_API_KEY']
    # Setup: Initialize your application components here
    battery = Initializer(
        database_path='./database_test',
        db_name='chroma',
        collection_name='test_collection',
        llm_name="mistral",
        llm_api_key=api_key
    )
    # Yield the setup component to the test
    yield battery
    # Teardown: Clean up after the test
    # Example: Remove the test database directory to ensure a clean slate for the next test
    shutil.rmtree('./database_test', ignore_errors=True)

@pytest.fixture
def db_adapter_setup(battery_setup):
    # The database initialization can stay as is, assuming it doesn't require special cleanup beyond removing the test database directory
    db_adapter = battery_setup.initialize_database()  # Initializes and returns the database and collection
    yield db_adapter
    # No additional teardown needed here since it's handled in the battery_setup fixture

@pytest.fixture
def llm_agent_setup(battery_setup):
    # Initialize the LLM agent with no additional teardown required
    llm_agent = battery_setup.initialize_llm()
    yield llm_agent
    # If the LLM agent requires cleanup, add it here