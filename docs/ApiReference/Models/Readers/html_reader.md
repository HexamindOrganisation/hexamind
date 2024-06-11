# HtlmReader

```python

class HtmlReader(htlm_content: str)
```

## Overview

The `HtmlReader` class converts the html format into markdown. It is a child object from the generic `IReader` class.

## Parameters

- `htlm_content` : str
    - The html content.

## Attributes

- `soup` : BeautifulSoup
    - The BeautifulSoup object of the html content.


## Methods

<div style="display: flex; flex-direction: row; justify-content: space-between; magin-bottom: 10px">
    <div style="flex: 1; padding: 8px;">
        ```python
        def convert_to_markdown(self) -> str
        ```
    </div>
    <div style="flex: 2; padding: 20px; ">
        Convert the html content to a markdown string.
    </div>
</div>

<hr style="border: none; border-top: 1px solid #ccc; margin 20px 0;">

## Usage Example

###### Code

```python

htlm_content = '<h1>Header</h1><p>Paragraph</p>'
reader = HtmlReader(htlm_content)
markdown = reader.convert_to_markdown()
print(markdown)
```

###### Output

```markdown

# Header

Paragraph
```