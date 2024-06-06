# WordReader

## Overview 

`WordReader` is a class that reads docx/doc files and convert the htlm format into markdown. It is a child object from the generic `IReader`interface. 

## Methods

### Constructor 

**Parameters**

- `path` : str
    - The path to the docx/doc file to be read.

### convert_to_markdown

Converts the word file content into markdown format.

**Returns**

- `str` : The markdown content.

##### Usage example

###### Code
```python 

docx_path = "path/to/docx/file.docx"
reader = WordReader(docx_path)
markdown_content = reader.convert_to_markdown()
print(markdown_content)
```