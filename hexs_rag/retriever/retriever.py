# Description: Retriever class that serves as the retrieval part of the RAG system
# Responsible for retrieving documents relevant to input query  

import os
from hexs_rag.model.model.block import Block
from hexs_rag.model.model.doc import Doc
from hexs_rag.llm.llm import LlmAgent

class Retriever:
    """
    Retriever class that serves as the retrieval part of the RAG system
    Responsible for retrieving documents relevant to input query  
    Attributes:
    - doc: doc.container # TODO
    - collection: # TODO
    - llmagent: # TODO
    - model: # TODO 
    """
    def __init__(self, doc: Doc = None, collection=None, llmagent: LlmAgent = None, model = "mistral-embed"):
        if not isinstance(doc, Doc) and doc is not None:
            raise TypeError("doc should be a Doc")
        if not isinstance(collection, type(None)):
            raise TypeError("collection should be a Collection")
        if not isinstance(llmagent, LlmAgent) and llmagent is not None:
            raise TypeError("llmagent should be a LlmAgent")
        if not isinstance(model, str):
            raise TypeError("model should be a string")
        self.doc = doc
        self.collection = collection
        self.llmagent = llmagent 
        self.model = model
        if self.doc:
            self.process_document()

    def process_document(self):
        """
        --------
        Applies the process_block function to each block in the document
        --------
        """
        for block in self.doc.blocks:
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
            new_blocks = block.separate_1_block_in_n(max_size=3000)
            for new_block in new_blocks:
                self.summarize_and_store(new_block)
        else:
            self.summarize_and_store(block)

    def summarize_and_store(self, block):
        """
        Creates a summary of the chunk content using the llmagent,
        then stores in the collection

        
        """
        summary = self.llmagent.summarize_paragraph_v2(prompt=block.content, 
                                                       title_doc=self.doc.title, 
                                                       title_para=block.title)
        summary = summary.split("<summary>")[1] if "<summary>" in summary else summary
        embedded_summary = self.get_embedding(summary)
        self.store_summary(summary, embedded_summary, block)

    def get_embedding(self, text):
        """
        Returns text sembeddings 
        """
        embeddings_batch_response = self.llmagent.client.embeddings(input=[text]) # TODO this needs to be generalizable. DONE
        return embeddings_batch_response.data[0].embedding

    def store_summary(self, summary, embedding, block):
        """
        adds summaries to collection
        """
        print(block.to_dict())
        self.collection.add(documents=[summary],
                            embeddings=[embedding],
                            ids=[block.index],
                            metadatas=[block.to_dict()])

    
    def summarize_by_hierarchy(self):
        """
        Summarizes blocks based on their hierarchical levels.
        """
        hierarchy = self.create_hierarchy(self.doc.blocks)
        deepest_blocks_indices = self.find_deepest_blocks(self.doc.blocks)
        print("Hierarchy levels identified:", hierarchy.keys())
        print("Deepest block indices:", deepest_blocks_indices)

        for level, level_blocks in hierarchy.items():
            if len(level_blocks) > 1 and any(block.index in deepest_blocks_indices for block in level_blocks):
                level_content = " ".join(block.content for block in level_blocks)
                level_summary = self.llmagent.summarize_paragraph_v2(
                    prompt=level_content,
                    title_doc=self.doc.title,
                    title_para=f"Summary of section: {level}"
                )
                self.store_summary(level_summary, level, level_blocks[0])

    def create_hierarchy(self, blocks):
        """
        Creates a hierarchical structure of the blocks based on their indices.
        """
        hierarchy = {}
        for block in blocks:
            levels = self.extract_levels(block.index)
            for level in levels:
                hierarchy.setdefault(level, []).append(block)
        return hierarchy

    def extract_levels(self, index):
        """
        Extracts all hierarchical levels from a block index.
        """
        parts = index.split('.')
        return ['.'.join(parts[:i]) for i in range(1, len(parts) + 1)]

    def find_deepest_blocks(self, blocks):
        """
        Identifies the deepest blocks in the hierarchy.
        """
        block_indices = {block.index for block in blocks}
        return {block.index for block in blocks if not any(
            idx != block.index and idx.startswith(block.index + '.') for idx in block_indices)}

    def similarity_search(self, queries: str, folder, document_or_folder, documents) -> {}:
        """
        Performs a similarity search in the collection based on given queries.

        Args:
            queries: A string or list of strings representing the query or queries.

        Returns:
            A list of Block objects that are similar to the given queries.
        """
        # Query the collection and retrieve blocks based on similarity.
        Dict_of_folders = os.getenv('FOLDERS_PATH')
        if not Dict_of_folders:
            raise EnvironmentError("FOLDERS_PATH environment variable is not set.")

        condition = {}
        if document_or_folder == "Collection":
            # Handle folder-based search
            if folder:
                # Fetch files from specified folders
                files_for_folder = [f["files"] for f in Dict_of_folders["entries"] if f["name"] in folder]
                if files_for_folder:
                    # Flatten the list of lists to a single list of files
                    condition = {"doc": {"$in": [file for sublist in files_for_folder for file in sublist]}}
        elif document_or_folder == "Document(s)":
            # Handle document-based search
            if documents:
                condition = {"doc": {"$in": documents}}
        embed_query = self.llmagent.client.embeddings(input=[queries])
        embed_query = embed_query.data[0].embedding

        res = self.collection.query(query_embeddings=embed_query, n_results=5, where=condition)
        print(res['metadatas'][0])
        block_dict_sources = res['metadatas'][0]
        distances = res['distances'][0]

        blocks = []
        for bd, d in zip(block_dict_sources, distances):
            b = Block().from_dict(bd)
            b.distance = d
            blocks.append(b)

        return blocks



    def keyword(self, queries,  keywords, folder, document_or_folder, documents) -> {}:
        """
        Performs a similarity search in the collection based on given queries.

        Args:
            queries: A string or list of strings representing the query or queries.

        Returns:
            A list of Block objects that are similar to the given queries.
        """
        Dict_of_folders = os.getenv('FOLDERS_PATH')
        if not Dict_of_folders:
            raise EnvironmentError("FOLDERS_PATH environment variable is not set.")
        
        condition = {}
        if document_or_folder == "Folder":
            # Handle folder-based search
            if folder:
                # Fetch files from specified folders
                files_for_folder = [f["files"] for f in Dict_of_folders["entries"] if f["name"] in folder]
                if files_for_folder:
                    # Flatten the list of lists to a single list of files
                    
                    condition = {"doc": {"$in": [file for sublist in files_for_folder for file in sublist]}}
        elif document_or_folder == "Document(s)":
            # Handle document-based search
            if documents:
                condition = {"doc": {"$in": documents},}
                
        embed_query = self.llmagent.client.embeddings(input=[queries])
        embed_query = embed_query.data[0].embedding
        blocks = []

        for i in range(len(keywords)):
            where_document={"$contains": keywords[i]}
            res = self.collection.query(query_embeddings=embed_query, n_results=4, where=condition,where_document=where_document)
            block_dict_sources = res['metadatas'][0]
            distances = res['distances'][0]

            for bd, d in zip(block_dict_sources, distances):
                b = Block().from_dict(bd)
                b.distance = d
                blocks.append(b)

        return blocks
