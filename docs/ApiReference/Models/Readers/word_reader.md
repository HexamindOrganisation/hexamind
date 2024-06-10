# WordReader

```python

class WordReader(path: str)
```

## Overview 

The `WordReader` class converts the word format into markdown. It is a child object from the generic `IReader` class.


## Parameters

- `path` : str
    - The path to the word file.

## Attributes 

- `path` : str
    - The path to the word file.

## Methods

<div style="display: flex; flex-direction: row; justify-content: space-between; magin-bottom: 10px">
    <div style="flex: 1; padding: 8px;">
        ```python
        def convert_to_markdown(self) -> str
        ```
    </div>
    <div style="flex: 2; padding: 20px; ">
        Convert the word file format to a markdown string.
    </div>
</div>

<hr style="border: none; border-top: 1px solid #ccc; margin 20px 0;">

## Usage Example

```python
path = 'path/to/word/file.docx'
reader = WordReader(path)
markdown = reader.convert_to_markdown()
``` 