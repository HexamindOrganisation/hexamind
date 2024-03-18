# Description: tests for whole rag system 

import os 
import pytest

from hxm_rag.initializer.initializer import Initializer
from hxm_rag.database.ingestion.ingestor import DocumentUploader
from hxm_rag.llm.llm.LlmAgent import LlmAgent
from hxm_rag.retriever.retriever import Retriever
from hxm_rag.model.model.doc import Doc 

from dotenv import load_dotenv

load_dotenv()

def test_llm_agent_setup():
    # test llm agent properties etc 
    # TODO implement for other llms agents than openai (in confest)
    pass

def test_db_adapter_setup():
    # TODO implement for other databases (in confest)
    pass

def test_whole_thing(llm_agent_setup, db_adapter_setup):
    doc = Doc(path="data/test_data/SampleData.xlsx", 
            include_images = False, 
            actual_first_page = 1)

    summarized_docs, embedded_summaries, block_list = doc.container.process_document(llm_agent_setup) 
    uploader = DocumentUploader(db_adapter_setup)
    uploader.upload_document(summarized_docs, embedded_summaries, block_list)
    
    # TODO check that document is in the database
    # TODO check that the summary is correctly being generated
    # TODO fix paragraph title coming out as an object
    retriever = Retriever(collection = db_adapter_setup.collection, 
                        llmagent = llm_agent_setup)
     # TODO check retriever algorithm

    
