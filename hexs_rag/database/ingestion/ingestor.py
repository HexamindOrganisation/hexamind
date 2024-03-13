from hexs_rag.model.model.doc import Doc
from hexs_rag.llm.llm import LlmAgent
from hexs_rag.utils.model.block import separate_1_block_in_n
from hexs_rag.database.adapters.AbstractDb import IDbClient
from hexs_rag.model.model.block import Block
from hexs_rag.llm.llm import LlmAgent

class Ingestor:
    """
    Ingestor class that serves as the ingestion part of the RAG system
    Responsible for retrieving documents relevant to input query  
    Attributes:
    - doc_container: doc.container # TODO
    - collection: # TODO
    - llmagent: # TODO
    - model: # TODO 
    """
    def __init__(self, clientdb : IDbClient, doc_container: Doc = None, llmagent: LlmAgent = None):
        # if not isinstance(doc_container, Doc.container) and doc_container is not None: # TODO
        #     raise TypeError("doc should be a Doc")
        # if not isinstance(collection, chromadb.api.models.Collection.Collection): # TODO generalise to all forms of db collection
        #     raise TypeError("collection should be a Collection")
        if not isinstance(llmagent, LlmAgent) and llmagent is not None:
            raise TypeError("llmagent should be a LlmAgent")
        self.doc_container = doc_container
        self.clientdb = clientdb
        self.llmagent = llmagent 
        if self.doc_container:
            self.process_document()

    def process_document(self):
        """
        --------
        Applies the process_block function to each block in the document
        --------
        """
        for block in self.doc_container.blocks:
            self.process_block(block)
        

    def process_block(self, block):
        """

        ---------------------------
        Method used to ingest blocks into the database.
        If the content is over 4000 characters
        The document content is divided into further chunks 
        Each chunk is then summarized and stored.
        If the content is less than 4000 characters it's directly summarized and stored 
        without further division.
        ---------------------------
        Attributes:
        block: 

        """
        if len(block.content) > 4000:
            new_blocks = separate_1_block_in_n(block, max_size=3000)
            for new_block in new_blocks:
                self.summarize_and_store(new_block)
        else:
            self.summarize_and_store(block)

    def summarize_and_store(self, block : Block):
        """
        Creates a summary of the chunk content using the llmagent,
        then stores in the collection

        
        """
        summary = self.llmagent.summarize_paragraph(prompt=block.content, 
                                                       title_doc=self.doc_container.title, 
                                                       title_para=block.title)
        summary = summary.split("<summary>")[1] if "<summary>" in summary else summary
        embedded_summary = self.llmagent.get_embedding(summary)

        self.clientdb.add_document(summary, embedded_summary, block)
        print(summary)

    
    def summarize_by_hierarchy(self):
        """
        Summarizes blocks based on their hierarchical levels.
        """
        hierarchy = self.create_hierarchy(self.doc_container.blocks)
        deepest_blocks_indices = self.find_deepest_blocks(self.doc_container.blocks)
        print("Hierarchy levels identified:", hierarchy.keys())
        print("Deepest block indices:", deepest_blocks_indices)

        for level, level_blocks in hierarchy.items():
            if len(level_blocks) > 1 and any(block.index in deepest_blocks_indices for block in level_blocks):
                level_content = " ".join(block.content for block in level_blocks)
                level_summary = self.llmagent.summarize_paragraph(
                    prompt=level_content,
                    title_doc=self.doc_container.title,
                    title_para=f"Summary of section: {level}"
                )
                self.clientdb.add_document(level_summary, level, level_blocks[0])