# ChunkExtractor

## Overview 

The `ChunkExtractor` class is responsible for extracting chunks from a document. It implements the differents default strategies to extract chunks from a document.

## Methods 

<div style="display: flex; flex-direction: row; justify-content: space-between; magin-bottom: 10px">
    <div style="flex: 1; padding: 8px;">
        ```python
        @staticmethod
        def extract_by_block(
            container: Container, 
            document_title : str, 
            tokenizer: ITokenizer
            ) -> List[Chunk]
        ```
    </div>
    <div style="flex: 2; padding: 20px; ">
        Extract a chunk as a block from Container/Block structure.
    </div>
</div>

<hr style="border: none; border-top: 1px solid #ccc; margin 20px 0;"> 

<div style="display: flex; flex-direction: row; justify-content: space-between; magin-bottom: 10px">
    <div style="flex: 1; padding: 8px;">
        ```python
        @staticmethod
        def extract_by_level(
            container: Container, 
            document_title: str, 
            tokenizer: ITokenizer
            ) -> List[Chunk]
        ```
    </div>
    <div style="flex: 2; padding: 20px; ">
        Extract a chunk by level from Container/Block structure.
    </div>
</div>

<hr style="border: none; border-top: 1px solid #ccc; margin 20px 0;"> 

<div style="display: flex; flex-direction: row; justify-content: space-between; magin-bottom: 10px">
    <div style="flex: 1; padding: 8px;">
        ```python
        @staticmethod
        def extract_by_section_number(
            container: Container, 
            document_title: str, 
            tokenizer: ITokenizer
            ) -> List[Chunk]
        ```
    </div>
    <div style="flex: 2; padding: 20px; ">
        Extract a chunk by section number from Container/Block structure.
    </div>
</div>

<hr style="border: none; border-top: 1px solid #ccc; margin 20px 0;"> 


## Usage Example

```python

chunks = ChunkExtractor.extract_by_block(self.root_container, self.title, self.tokenizer)

```