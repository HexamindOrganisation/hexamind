import os
from unittest.mock import MagicMock
import pytest
import chromadb 
import sys
import os
from dotenv import load_dotenv

from hexs_rag.initializer.initializer import Initializer

DATABASE_PATH = os.getenv('DATABASE_PATH')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')

def test_intialization():
    tst = Initializer()
    tst.initialize_database()
    directory_created = os.path.exists(str(DATABASE_PATH))
    assert directory_created == True


# @pytest.fixture
# def filesystem_mock(mocker):
#     """
#     Mocks filesystem operations to avoid actual file system interaction during the test.
#     Specifically, it mocks 'os.path.exists' to always return False, simulating a non-existing path,
#     and 'os.makedirs' to do nothing (avoiding directory creation).
#     """
#     mocker.patch("os.path.exists", return_value=False)
#     mocker.patch("os.makedirs")

# @pytest.fixture
# def chromadb_mock(mocker):
#     """
#     Mocks the 'chromadb.PersistentClient' and its method 'get_or_create_collection'.
#     This avoids initializing a real database connection and instead uses a mock object.
#     """
#     collection_mock = MagicMock()
#     client_mock = MagicMock()
#     client_mock.get_or_create_collection.return_value = collection_mock
#     mocker.patch("your_module.chromadb.PersistentClient", return_value=client_mock)
#     return client_mock, collection_mock

# def test_initialize_database(chromadb_mock):
#     """
#     Tests the 'initialize_database' method of the 'Initializer' class.
#     It checks that the database path is correctly checked and created if necessary,
#     and that the database client and collection are correctly initialized and returned.
#     """
#     # Instantiate the Initializer 
#     initializer = Initializer()

#     # Call the method under test
#     client_db, collection = initializer.initialize_database()

#     # Verify os.path.exists was called with the correct path
#     os.path.exists.assert_called_once_with(DATABASE_PATH)
#     # Verify os.makedirs was called with the correct path, simulating directory creation
#     os.makedirs.assert_called_once_with(DATABASE_PATH)
#     # Verify chromadb.PersistentClient was instantiated with the correct database path
#     chromadb.PersistentClient.assert_called_once_with(DATABASE_PATH)
#     # Verify the correct collection was retrieved/created
#     client_db.get_or_create_collection.assert_called_once_with(COLLECTION_NAME)

#     # Assert the returned client_db and collection match the mocked objects
#     assert client_db == chromadb_mock[0]
#     assert collection == chromadb_mock[1]



