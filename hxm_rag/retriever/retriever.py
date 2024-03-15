# Description: Retriever class that serves as the retrieval part of the RAG system
# Responsible for retrieving documents relevant to input query

import os

from hxm_rag.llm.llm import LlmAgent
from hxm_rag.model.model.block import Block


class Retriever:
    """
    Retriever class that serves as the retrieval part of the RAG system
    Responsible for retrieving documents relevant to input query  
    Attributes:
    - collection: # TODO
    - llmagent: # TODO
    - model: # TODO 
    """

    def __init__(
        self, collection=None, llmagent: LlmAgent = None, model="mistral-embed"
    ):
        # if not isinstance(collection, chromadb.api.models.Collection.Collection): # TODO generalise to all forms of db collection
        #     raise TypeError("collection should be a Collection")
        if not isinstance(llmagent, LlmAgent) and llmagent is not None:
            raise TypeError("llmagent should be a LlmAgent")
        if not isinstance(model, str):
            raise TypeError("model should be a string")
        self.collection = collection
        self.llmagent = llmagent
        self.model = model

    def similarity_search(
        self, queries: str, folder, document_or_folder, documents
    ) -> dict:
        """
        Performs a similarity search in the collection based on given queries.

        Args:
            queries: A string or list of strings representing the query or queries.
            folder:
            document_or_folder:
            documents:

        Returns:
            A list of Block objects that are similar to the given queries.
        """
        # Query the collection and retrieve blocks based on similarity.
        Dict_of_folders = os.getenv("FOLDERS_PATH")
        if not Dict_of_folders:
            raise EnvironmentError("FOLDERS_PATH environment variable is not set.")

        condition = {}
        if document_or_folder == "Collection":
            # Handle folder-based search
            if folder:
                # Fetch files from specified folders
                files_for_folder = [
                    f["files"]
                    for f in Dict_of_folders["entries"]
                    if f["name"] in folder
                ]
                if files_for_folder:
                    # Flatten the list of lists to a single list of files
                    condition = {
                        "doc": {
                            "$in": [
                                file for sublist in files_for_folder for file in sublist
                            ]
                        }
                    }
        elif document_or_folder == "Document(s)":
            # Handle document-based search
            if documents:
                condition = {"doc": {"$in": documents}}
        embed_query = self.llmagent.client.embeddings(input=[queries])
        embed_query = embed_query.data[0].embedding

        res = self.collection.query(
            query_embeddings=embed_query, n_results=5, where=condition
        )
        print(res["metadatas"][0])
        block_dict_sources = res["metadatas"][0]
        distances = res["distances"][0]

        blocks = []
        for bd, d in zip(block_dict_sources, distances):
            print("dict for block: \n\n", bd)
            b = Block().from_dict(bd)  # creates a block object from a dictionary
            b.distance = d  # the distance has to be set manually
            blocks.append(b)
        return blocks

    def keyword(self, queries, keywords, folder, document_or_folder, documents) -> dict:
        """
        Performs a similarity search in the collection based on given queries.

        Args:
            queries: A string or list of strings representing the query or queries.
            keywords:
            folder:
            document_or_folder:
            documents:
            
        Returns:
            A list of Block objects that are similar to the given queries.
        """
        Dict_of_folders = os.getenv("FOLDERS_PATH")
        if not Dict_of_folders:
            raise EnvironmentError("FOLDERS_PATH environment variable is not set.")

        condition = {}
        if document_or_folder == "Folder":
            # Handle folder-based search
            if folder:
                # Fetch files from specified folders
                files_for_folder = [
                    f["files"]
                    for f in Dict_of_folders["entries"]
                    if f["name"] in folder
                ]
                if files_for_folder:
                    # Flatten the list of lists to a single list of files

                    condition = {
                        "doc": {
                            "$in": [
                                file for sublist in files_for_folder for file in sublist
                            ]
                        }
                    }
        elif document_or_folder == "Document(s)":
            # Handle document-based search
            if documents:
                condition = {
                    "doc": {"$in": documents},
                }

        embed_query = self.llmagent.client.embeddings(input=[queries])
        embed_query = embed_query.data[0].embedding
        blocks = []

        for i in range(len(keywords)):
            where_document = {"$contains": keywords[i]}
            res = self.collection.query(
                query_embeddings=embed_query,
                n_results=4,
                where=condition,
                where_document=where_document,
            )
            block_dict_sources = res["metadatas"][0]
            distances = res["distances"][0]

            for bd, d in zip(block_dict_sources, distances):
                print(f"(retriever.py)\n dict for block: \n\n{bd}")
                b = Block().from_dict(bd)
                b.distance = d
                blocks.append(b)

        return blocks
