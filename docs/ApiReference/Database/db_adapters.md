# Database Adpaters Factory

## Overview

The database adapters are responsible for interfacing with vector databases. 

Currently, hxm_rag supports only two databases which are chromadb and Elasticsearch. Please note that the Elasticsearch database is still under development.

A factory class is  available to create the database adapter based on the database type.

## DbAdapterFactory

The `DbAdapterFactory` class is used tp instanciate the proper database adapter based on the database type.

#### create_adapter

Create a database adapter based on the database type.

**Parameters:**

- `db_name` (str): The name of the database. ('chroma' or 'elasticsearch')
- `collection_name` (str): The name of the collection in the database. Default is None.
- `kwargs` (dict): The keyword arguments to pass to the database adapter.
    - ChromaDbAdapter:
        - `database_path` (str): The path to the chroma file.

**Returns:**

- Database Adapter (`IDbClient`): Returns on instance of the database adpater. This type will always be an `IDbClient`.  
    - `ChromaDbAdapter`: If the db_name is 'chroma'.
    - `ElasticSearchAdapter`: If the db_name is 'elasticsearch'.

##### Usage Example

###### Code
```py

db_adapter = DbAdapterFactory.create_adapter(db_name='chroma', collection_name='chunks', database_path='path/to/chroma.db')

print(type(db_adapter))
```

###### Output
```py 
<class 'hxm_rag.database.adapters.ChromaDbAdapter.ChromaDbAdapter'>
```


## IDbClient

Each of the adapters implement these methods from the `IDbClient` class. Basically all of the CRUD operations.

-   `add_document`: Add a document to the database.
-   `get_document`: Get a document from the database.
-   `delete_document`: Delete a document from the database.
-   `update_document`: Update a document in the database.
-   `search`: Search for documents in the database.