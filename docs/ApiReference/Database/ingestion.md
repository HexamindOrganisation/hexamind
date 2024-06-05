# Ingestor

## Overview

The ingestor is the component responsible for ingesting the data into the vector databases. The ingestor creates the embeddings, populate content and metadata, and store the data in the database. 

## Ingestor

**Parameters:**

- `db_client` (AbstractDb) : The database client to use.
- `llm_agent` (LlmAgent): The LLM agent to use.

### Methods

#### store_container

Store a container in the database. 

The method will ingest recursively all the container from the input container. When we talk about ingesting container that means ingesting the content of the container. Each content as associated metadata,  embeddings and ids.

*To get more information about the container, check the [Container](model/model/container.md) documentation.*

**Parameters:**

- `container` (Container): The container to store.

##### Usage Example

###### Code

```py

ingestor = Ingestor(db_client=ChromaDbAdapter(database_path='path/to/chroma.db'), llm_agent=llm_agent)

dict_structure = WordReader("path/to/word_file").get_document_structure()
document = Document(dict_structure)
doc.root_container.get_embeddings(llm_agent=llm_agent)
ingestor.store_container(container=document.root_container)

```

#### store_container_summaries

Store the summaries of a container in the database.

This method will ingest recursively all the summary associated to a container. 

*To get more information about the container, check the [Container](model/model/container.md) documentation.*

**Parameters:**

- `container` (Container): The container to store.

##### Usage Example

###### Code
```py

ingestor = Ingestor(db_client=ChromaDbAdapter(database_path='path/to/chroma.db'), llm_agent=llm_agent)

dict_structure = WordReader("path/to/word_file").get_document_structure()
document = Document(dict_structure)
doc.root_container.get_summaries(llm_agent=llm_agent)
ingestor.store_container(container=document.root_container)

```

#### ingest_content

Ingest the content of a document. This method streamlines the whole process of ingesting a document. From creating the embeddings to storing the data in the database. So it will use the `store_container` method. 

**Parameters:**

- `document` (Document): The document to ingest.

##### Usage Example

###### Code

```py

ingestor = Ingestor(db_client=ChromaDbAdapter(database_path='path/to/chroma.db'), llm_agent=llm_agent)

dict_structure = WordReader("path/to/word_file").get_document_structure()

document = Document(dict_structure)

ingestor.ingest_content(document=document)

```

#### ingest_summaries

Ingest the summaries of a document. This method streamlines the whole process of ingesting a document summaries. From creating the embeddings to storing the data in the database. So it will use the `store_container_summaries` method.

**Parameters:**

- `document` (Document): The document to ingest.

##### Usage Example

###### Code

```py

ingestor = Ingestor(db_client=ChromaDbAdapter(database_path='path/to/chroma.db'), llm_agent=llm_agent)

dict_structure = WordReader("path/to/word_file").get_document_structure()

document = Document(dict_structure)

ingestor.ingest_summaries(document=document)

```

### How to import

```py

from hexamind import Ingestor

```