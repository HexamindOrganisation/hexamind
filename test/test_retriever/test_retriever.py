import unittest
from unittest.mock import patch, MagicMock
from hexamind.retriever.retriever import Retriever 
from hexamind.model.model.document import   Document as Doc
from hexamind.llm.llm.LlmAgent import LlmAgent
from hexamind.initializer.initializer import Initializer

class TestRetriever(unittest.TestCase):
    """
    Test suite for the Retriever class.
    """

    def setUp(self):
        """
        Set up environment before each test.
        """

        # Create a deep mock to automatically mock attribute calls.
        self.llmagent = MagicMock(spec=LlmAgent, client=MagicMock())
        # Now explicitly set up the embeddings method to return what you expect.
        self.llmagent.client.embeddings.return_value = MagicMock(data=[MagicMock(embedding='mock_embedding')])
        # Instantiate the Retriever with the mocked LlmAgent.
        self.retriever = Retriever(llmagent=self.llmagent)
        self.retriever.collection = MagicMock()
        self.retriever.collection.query.return_value = {'metadatas': [['mock_data','mock_data2']], 'distances': [0.2,0.1]}

    def test_init(self):
        """
        Test __init__ method to ensure it initializes attributes correctly.
        """
        self.assertIs(self.retriever.llmagent, self.llmagent)
    
    # @patch('hexs_rag.retriever.retriever.Retriever.extract_levels')
    # def test_create_hierarchy(self, mock_extract_levels):
    #     """
    #     Test create_hierarchy method.
    #     Mock extract_levels to return predefined levels for testing.
    #     """
    #     mock_extract_levels.side_effect = lambda x: [x]
    #     blocks = [MagicMock(index='1'), MagicMock(index='2')]
    #     hierarchy = self.retriever.create_hierarchy(blocks)
    #     self.assertTrue('1' in hierarchy and '2' in hierarchy)
    #     # Additional assertions to validate the structure of the hierarchy.

    # def test_extract_levels(self):
    #     """
    #     Test extract_levels method for correct extraction of hierarchical levels.
    #     """
    #     index = '1.2.3'
    #     expected_levels = ['1', '1.2', '1.2.3']
    #     levels = self.retriever.extract_levels(index)
    #     self.assertEqual(levels, expected_levels)
    
    # def test_find_deepest_blocks(self):
    #     """
    #     Test find_deepest_blocks to ensure it identifies deepest blocks correctly.
    #     """
    #     blocks = [MagicMock(index='1.1'), MagicMock(index='1.2'), MagicMock(index='1.1.1')]
    #     deepest_blocks = self.retriever.find_deepest_blocks(blocks)
    #     self.assertIn('1.2', deepest_blocks)
    #     self.assertIn('1.1.1', deepest_blocks)
    #     self.assertNotIn('1.1', deepest_blocks)
    
# TODO delete later
# class TestRetriever_with_real_data:
#     def setUp(self):
#         """
#         Set up environment before each test.
#         """
#         battery = Initializer( # initializes instance attributes
#         database_path = './database_test', 
#         db_name = 'chroma', # chroma db name
#         collection_name = 'test_collection', 
#         llm_name = "mistral", # either mistral or openai 
#         llm_api_key = 'n70UAHiVwZLbJW5jj1xpT5zRDCRtpozp'
#         )

#         db_adapter = battery.initialize_database() # Initializes and returns the database and collection
#         llm_agent = battery.initialize_llm()

#         doc = Doc(path="./hexs_rag/data/test_data/SampleData.xlsx", 
#                 include_images = False, 
#                 actual_first_page = 1)

#         retriever = Retriever( 
#                         collection = db_adapter.collection, 
#                         llmagent = llm_agent)

#         retriever.similarity_search(queries=query, folder=folder, document_or_folder=doc_or_folder, documents=documents)
