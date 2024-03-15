import os 
import pytest

from hexs_rag.initializer.initializer import Initializer
from hexs_rag.database.ingestion.ingestor import Ingestor
from hexs_rag.llm.llm.LlmAgent import LlmAgent
from hexs_rag.retriever.retriever import Retriever
from hexs_rag.model.model.doc import Doc 



def test_whole_thing(llm_agent_setup, db_adapter_setup):
    doc = Doc(path="../hexs_rag/data/test_data/SampleData.xlsx", 
            include_images = False, 
            actual_first_page = 1)

    ingestor = Ingestor(doc_container = doc.container, 
                        clientdb = db_adapter_setup,
                        llmagent = llm_agent_setup)
    # TODO check that document is in the database
    # TODO check that the summary is correctly being generated
    retriever = Retriever(collection = db_adapter_setup.collection, 
                        llmagent = llm_agent_setup)
    # TODO check retriever algorithm
    
