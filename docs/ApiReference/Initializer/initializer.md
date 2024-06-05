# Initializer

## Overview

The purpose of this classs is to provide a simple and fast way to initialize your database and your Llm agent. 
This initializer will use the two factories :

- `DbAdapterFactory` to create the database
- `LlmAdapterFactory` to create the llm client

**Attributes:**

- `db_name` (str): The name of the database.
- `database_path` (str): The path to the database.
- `collection_name` (str): The name of the collection in the database.
- `llm_name` (str): The name of the llm model you want to use
- `llm_api_key` (str): The api key of the llm model you want to use
- `model` (str): The model to use for the llm agent.
- `embed_model` (str): The model to use for the embeddings.

##### Usage Example

###### Code

```py

initializer = Initializer(
    db_name='chroma',
    database_path='path/to/chroma.db',
    collection_name='chunks',
    llm_name='mistral',
    llm_api_key='api_key',
    model='mistral-large',
    embed_model='mistral-embed')
```
##### output

```py

<class 'hxm_rag.initializer.initializer.Initializer'>
```
### Methods

#### initialize_database

This method instanciate the database client based on the configuration provided in the initializer.

**Returns:**

- `IDbClient`: The database client.

##### Usage Example

###### Code

```py

db_adapter = initializer.initialize_database()

print(type(db_adapter))
```

##### output

```py

<class 'hxm_rag.database.adapters.ChromaDbAdapter.ChromaDbAdapter'>

```

#### initialize_llm

This method instanciate the llm agent based on the configuration provided in the initializer.

**Returns:**

- `LlmAgent`: The llm agent.

##### Usage Example

###### Code

```py

llm_agent = initializer.initialize_llm()

print(type(llm_agent))
```

##### output

```py

<class 'hxm_rag.llm.llm.LlmAgent.LlmAgent'>

```