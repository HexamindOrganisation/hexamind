# Tokenizer

```python 

class Tokenizer()

```

## Overview 

The `Tokenizer` class is responsible for tokenizing a text. It is used in particular by the `ChunkExtractor` class to extract chunks from a document. 
The default hexamind Tokenizer uses the MistralTokenizer. 

You can implement your own tokenizer by creating a child class of the `ITokenizer` interface define as follow:

```python

class ITokenizer(ABC):
    @abstractmethod
    def tokenize(self, text: str) -> List[str]:
        pass

    @abstractmethod
    def decode(self, tokens: List[str]) -> str:
        pass

    @abstractmethod
    def count_tokens(self, text: str) -> int:
        pass

```

## Attributes

- `tokenizer` : The tokenizer used to tokenize the text. 
    - Here `MistralTokenizer.from_model("open-mixtral-8x22b")`


## Methods

<div style="display: flex; flex-direction: row; justify-content: space-between; magin-bottom: 10px">
    <div style="flex: 1; padding: 8px;">
        ```python
        def tokenize(self, text: str) -> List[int]
        ```
    </div>
    <div style="flex: 2; padding: 20px; ">
        Transform sequence of characters into a sequence of tokens.
    </div>
</div>

<hr style="border: none; border-top: 1px solid #ccc; margin 20px 0;"> 

<div style="display: flex; flex-direction: row; justify-content: space-between; magin-bottom: 10px">
    <div style="flex: 1; padding: 8px;">
        ```python
        def decode(self, tokens: List[int]) -> str
        ```
    </div>
    <div style="flex: 2; padding: 20px; ">
        Transform sequence of tokens into a sequence of characters.
    </div>
</div>

<hr style="border: none; border-top: 1px solid #ccc; margin 20px 0;"> 

<div style="display: flex; flex-direction: row; justify-content: space-between; magin-bottom: 10px">
    <div style="flex: 1; padding: 8px;">
        ```python
        def count_tokens(self, text: str) -> int
        ```
    </div>
    <div style="flex: 2; padding: 20px; ">
        Count the number of tokens in a text.
    </div>
</div>

<hr style="border: none; border-top: 1px solid #ccc; margin 20px 0;"> 
    
## Usage Example

```python

tokenizer = Tokenizer()
tokens = tokenizer.tokenize("Hello, World!")

```
