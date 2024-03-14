from hexs_rag.initializer.initializer import Initializer
from hexs_rag.database.ingestion.ingestor import Ingestor
from hexs_rag.llm.llm.LlmAgent import LlmAgent
from hexs_rag.retriever.retriever import Retriever
from hexs_rag.model.model.doc import Doc 

def test_whole_thing():
    
    battery = Initializer( # initializes instance attributes
        database_path = './database_test', 
        collection_name = 'test_collection', 
        llm_name = "mistral", # either mistral or openai
        llm_api_key = 'n70UAHiVwZLbJW5jj1xpT5zRDCRtpozp'
    ) 

    client_db, collection = battery.initialize_database() 
    llm_agent = battery.initialize_llm()


    doc = Doc(path="/Users/maxbeales/Desktop/hexamind/hexs_rag/data/test_data/SampleData.xlsx", 
            include_images = False, 
            actual_first_page = 1)

    ingestor = Ingestor(doc_container = doc.container, 
                    collection = collection, 
                    llmagent = llm_agent)
    # TODO check that document is in the database
    # TODO check that the summary is correctly being generated
    retriever = Retriever(doc_container = doc.container, 
                        collection = collection, 
                        llmagent = llm_agent)
    # TODO check retriever algorithm
    
