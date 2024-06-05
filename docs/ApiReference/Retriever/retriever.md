# Retriever 

## Overview

The Retriever is the component that will proceed the data retrieval from the database. It will be responsible for the similarity search. 

## Properties

**Attributes**

- `db_client`(IDbClient): The database client that will be used to retrieve the data.
- `llm_agent`(LLMAgent): The agent that will be used. 

## Methods

#### similarity_search

Perform a similarity search on the database.

**Parameters**

- `query`(str): The query to search for.


**Returns**

- `List[Block]`: The list of blocks retrieved from the database.

##### Usage Example

###### Code

```py

retriever = Retriever(db_client, llm_agent)

blocks = retriever.similarity_search("How to create a new document?")

```
