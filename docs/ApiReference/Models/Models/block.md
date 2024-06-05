# Block

## Overview 

The Block is the leaf node of the hexamind data representation. It is the only element that can contain raw content. The Block doesn't have any behavior. 
```mermaid

%%{init: {'themeVariables': { 'primaryColor': '#ffdddd'}}}%%
graph TD
    classDef red fill:#ffdddd,stroke:#ff0000,stroke-width:2px;

    subgraph Level0
        container1["Root Container"]
    end
    
    subgraph Level1
        container2["Container"]
        container3["Container"]
    end
    
    subgraph Level2
        container4["Container"]
        container5["Container"]
        container6["Container"]
        container7["Container"]
    end
    
    subgraph Level3
        block1["Block"]
        block2["Block"]
        block3["Block"]
        block4["Block"]
        class block1,block2,block3,block4 red
    end

    container1 --> container2
    container1 --> container3
    container2 --> container4
    container2 --> container5
    container3 --> container6
    container3 --> container7
    container4 --> block1
    container5 --> block2
    container6 --> block3
    container7 --> block4

```

### Rules 

The following rules are applied when creating this structure : 

- A container can contain other containers or blocks
- A block can only contain raw content and don't have any children
- A container can contain multiple children
- A block is always contained by it own parent container

### Properties

A Block, as well as a Container, inherit from the same abstract class `Element`.

The Block is the object use in the leaf node of the hexamind tree representation of a document. But it is also the object retrieve by the retriver in the vector db. Every sources retrieved is then converted to a block object, and a distance from the query is associated to it.

## Properties

**Constructor Parameters**

- `content`(str): The content of the block.
- `parent_document`(Document): The parent document of the block.
- `parent_container`(Container): The parent container of the block.
- `distance`(int): In the RAG model, represents the distance between the block and the query. 

**Attributes**

- `content`(str): The content of the block.
- `parent_document`(Document): The parent document of the block.
- `parent_container`(Container): The parent container of the block.
- `distance`(int): In the RAG model, represents the distance between the block and the query.
- `level`(int): The level of the block in the document.

## Methods

#### get_content

Return the content of the block.

#### to_dict

Return a dictionary representation of the block.

#### from_metadata

Create a block object from a metadata dictionary. This method is used to create a block object from the vector db.

**Parameters**

- `text_content`(str): The content of the block.
- `metadata`(dict): The metadata of the block.
- `meta_distance`(int): The distance of the block from the query.

**Returns**

- `Block`: The block object created from the metadata.

##### Usage Example

###### Code

```py

blocks = []
for content, metadata, distance in zip(contents, metadatas, distances):
    block = Block.from_metadata(content, metadata, distance)
    blocks.append(block)

```


