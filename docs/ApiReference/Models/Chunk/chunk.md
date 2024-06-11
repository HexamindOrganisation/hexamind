# Chunk

```python

class Chunk(
    content: str, 
    container_uid: str, 
    title: Optional[str] = None, 
    level: Optional[int] = None, 
    document_title : Optional[str] = None, 
    section_number: Optional[str] = None)

```

## Overview 

A chunk is a representation of a segment of a document with specific attributes. This is the representation used in RAG application to store data into the database.

## Parameters

- `content` : str
    - The content of the chunk.

- `container_uid` : str
    - The unique identifier of the container where the content belongs.

- `title` : Optional[str]
    - The title of the container where the content belongs.

- `level` : Optional[int]
    - The level of the container where the content belongs.

- `document_title` : Optional[str]
    - The title of the document where the content belongs.

- `section_number` : Optional[str]
    - The section number of the container where the content belongs.

## Attributes 

- `uid` : str
    - The unique identifier of the chunk.

- `content` : str
    - The content of the chunk.

- `container_uid` : str
    - The unique identifier of the container where the content belongs.

- `title` : Optional[str]
    - The title of the container where the content belongs.

- `level` : Optional[int]
    - The level of the container where the content belongs.

- `document_title` : Optional[str]
    - The title of the document where the content belongs.

- `section_number` : Optional[str]
    - The section number of the container where the content belongs.

- `embeddings` : Optional[ndarray]
    - The embeddings of the content.

- `metadata` : Optional[Dict[str, Any]]
    - The metadata of the chunk.


## Methods

<div style="display: flex; flex-direction: row; justify-content: space-between; magin-bottom: 10px">
    <div style="flex: 1; padding: 8px;">
        ```python
        def add_metadata(
            self, 
            key: str, 
            value: Any
            ) -> None
        ```
    </div>
    <div style="flex: 2; padding: 20px; ">
        Add custom metadatas to the chunk. This can be used to store additional information about the chunk.
    </div>
</div>

<hr style="border: none; border-top: 1px solid #ccc; margin 20px 0;">

<div style="display: flex; flex-direction: row; justify-content: space-between; magin-bottom: 10px">
    <div style="flex: 1; padding: 8px;">
        ```python
        def generate_embeddings(
            self, 
            ll_agent: LlmAgent
            ) -> None
        ```
    </div>
    <div style="flex: 2; padding: 20px; ">
        Use a language model to generate embeddings for the content of the chunk. 
    </div>
</div>

<hr style="border: none; border-top: 1px solid #ccc; margin 20px 0;">

<div style="display: flex; flex-direction: row; justify-content: space-between; magin-bottom: 10px">
    <div style="flex: 1; padding: 8px;">
        ```python
        def to_dict(self) -> Dict[str, Any]
        ```
    </div>
    <div style="flex: 2; padding: 20px; ">
        Serialize the chunk into a dictionary.
    </div>
</div>

<hr style="border: none; border-top: 1px solid #ccc; margin 20px 0;">


## Usage Example

```python

chunks = []
for i in range(num_chunks):
            start_idx = i * ChunkExtractor.MAX_TOKENS
            end_ids = start_idx + ChunkExtractor.MAX_TOKENS
            chunk_content = tokenizer.decode(tokens[start_idx:end_ids])
            chunk = Chunk(
                content=chunk_content,
                container_uid=container_uid,
                title=title,
                level=level,
                document_title=document_title,
                section_number=section_number
            ) # Creating a chunk
            chunks.append(chunk)

```