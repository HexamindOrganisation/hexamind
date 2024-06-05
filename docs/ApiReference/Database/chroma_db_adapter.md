# ChromaDbAdapter

## Overview

The `ChromaDbAdapter` class is used to interface with the chroma database. This class implements every CRUd methid inherited from the `IDbClient` class.

## ChromaDbAdapter

**Attributes:**

- `client` (ChromaClient): The chroma client used to interface with the database.
- `collection_name` (str): The name of the collection in the database.

### Methods

#### add_document

Add a document to the chroma database.

**Parameters:**

- `document` (dict): The chunk to store.
- `embedding`(List[float]): The embeddings related to the chunk.
- `ids` (int): The ids of the chunk.
- `metadata` (dict): The metadatas of the chunk.

##### Usage Example

###### Code
```py
db_client = ChromaDbAdapter(database_path='path/to/chroma.db')

for doc, embedding, id, metadata in zip(container.chunks, container.embeddings, container.chunk_ids, container.metadatas):
    db_client.add_document(
        document=doc,
        embedding=embedding,
        ids=id,
        metadatas=metadata
        )
```

#### get_document

**Parameters:**

- `id` (int): The id of the document to retrieve.

**Returns:**

- `document` (dict): The document retrieved from the database.

##### Usage Example

###### Code

```py
db_client = ChromaDbAdapter(database_path='path/to/chroma.db')

doc = db_client.get_document(id=1)
```

#### delete_document

**Parameters:**

- `id` (int): The id of the document to delete.

##### Usage Example

###### Code

```py
db_client = ChromaDbAdapter(database_path='path/to/chroma.db')

db_client.delete_document(id=1)
```

#### update_document

*Documentation coming soon.*

#### search

**Parameters:**

- `query` (str): The query to search for.
- `num_results` (int): The number of results to return.

**Returns:**

- `results` (List[dict]): The results of the search.

##### Usage Example

###### Code

```py

db_client = ChromaDbAdapter(database_path='path/to/chroma.db')
query_embedding = np.random.rand(1, 768)
results = db_client.search(query=query_embedding, num_results=10)
```

#### get 

This method is exclusive to the `ChromaDbAdapter` class. It is used to get all the documents in the database.

**Returns:**

- `documents` (List[dict]): The documents in the database.

##### Usage Example

###### Code

```py

db_client = ChromaDbAdapter(database_path='path/to/chroma.db')
documents = db_client.get()
```