from hxm_rag.database.adapters.AbstractDb import IDbClient
from hxm_rag.llm.llm.LlmAgent import LlmAgent
from hxm_rag.model.model.block import Block

class Retriever: 
    def __init__(self, db_client: IDbClient, llm_agent: LlmAgent):
        self.db_client = db_client
        self.llm_agent = llm_agent
    
    def similarity_search(self, query):
        query_embedding = self.llm_agent.get_embedding(query)
        results = self.db_client.search(query_embedding, num_results=10)

        contents = results['documents'][0]
        metadatas = results['metadatas'][0]
        distances = results['distances'][0]

        blocks = []
        for content, metadata, distance in zip(contents, metadatas, distances):
            block = Block.from_metadata(content, metadata, distance)
            blocks.append(block)

        return blocks

