# MkBuilder

## Overview

The `MkBuilder` is used to created the Container/Block tree structure that represents a document. 

## Methods

<div style="display: flex; flex-direction: row; justify-content: space-between; magin-bottom: 10px">
    <div style="flex: 1; padding: 8px;">
        ```python
        @classmethod
        def from_markdown(
            cls, 
            markdown_content : str, 
            document_title : str) -> Container:
        ```
    </div>
    <div style="flex: 2; padding: 20px; ">
        Build the Container/Block tree structure that represents a document.
    </div>
</div>

<hr style="border: none; border-top: 1px solid #ccc; margin 20px 0;">

## Usage Example

```python

markdown_content = """
# Title

This is a paragraph."""

document_title = "Title"

container = MkBuilder.from_markdown(markdown_content, document_title)

print(container)

```

## Output

```
Root container, Level: 0
└── Container, Level: 1, Section number: 1
    └── Container, Level: 1, Section number: 1
        └── Block, Level: 1, Section number: 1

```
