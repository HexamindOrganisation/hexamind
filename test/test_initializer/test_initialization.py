import os
import pytest
import chromadb 
from unittest.mock import patch, MagicMock
import os
import logging

# import intialization module from hexs_rag directory
from hexamind.initializer.initializer import Initializer

# Mock the environment variables for the test
@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv('DATABASE_PATH', './database_test')
    monkeypatch.setenv('COLLECTION_NAME', 'test_collection')
    monkeypatch.setenv('LLM_NAME', 'mistral')
    monkeypatch.setenv('LLM_API_KEY', 'test_api')

@pytest.fixture
def mock_chromadb(monkeypatch):
    """
    Creates a mock version of the chromadb client
    """
    mock_client = MagicMock()
    mock_collection = MagicMock()
    mock_client.get_or_create_collection.return_value = mock_collection
    monkeypatch.setattr(chromadb, 'PersistentClient', MagicMock(return_value=mock_client))
    return mock_client

def test_collection_creation(mock_env):
    with patch('chromadb.PersistentClient') as mock_chromadb:
        # DATABASE_PATH and COLLECTION_NAME are read from the environment
        mock_client = MagicMock()
        mock_collection = MagicMock()
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_chromadb.return_value = mock_client


        database_path = os.getenv('DATABASE_PATH')
        initializer = Initializer()
        _, collection = initializer.initialize_database()

        print(f"Database directory created at: {initializer}")
        # Verify the PersistentClient was initialized with the correct path
        mock_chromadb.assert_called_once_with(database_path)
    # Verify get_or_create_collection was called with the correct collection name
        mock_chromadb.return_value.get_or_create_collection.assert_called_once_with(os.getenv('COLLECTION_NAME'))

        assert os.getenv('COLLECTION_NAME') == 'test_collection'
        assert os.getenv('DATABASE_PATH') == './database_test'


def test_create_directory(fs, mock_env, mock_chromadb):
    # `fs` is the fake filesystem provided by pyfakefs
    # DATABASE_PATH and COLLECTION_NAME are read from the environment
    database_path = os.getenv('DATABASE_PATH')
    # Ensure the directory does not exist before calling the function
    assert not os.path.exists(database_path)
    # Instantiate the class and call the method to initialize the database
    initializer = Initializer()
    client_db, collection = initializer.initialize_database()
    assert os.path.exists(database_path)

# Test to check the correct initialization of the database client and collection
def test_database_client_and_collection_initialization(mock_chromadb, mock_env):
    # Create a mock client and mock collection, configuring their behavior
    mock_client = MagicMock()
    mock_client.get_or_create_collection.return_value = MagicMock(name="initialized_collection")
    mock_chromadb.return_value = mock_client
    
    # Instantiate the Initializer and initialize the database
    initializer = Initializer()
    client_db, collection = initializer.initialize_database()
    
    # Assert that both the database client and collection are not None 
    assert client_db is not None
    assert collection is not None

def test_llm_initialization(mock_env):
    # Instantiate the Initializer and initialize the LLM client
    initializer = Initializer()
    llm_agent = initializer.initialize_llm()
    
    # Assert that the LLM client is not None
    assert llm_agent is not None


