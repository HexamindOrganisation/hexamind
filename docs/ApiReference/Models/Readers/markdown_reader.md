# MardownReader

## Overview

`MarkdownReader` is a class that reads markdown content and convert the format into the nested dictionnary structure using `MkTransformer`. It is a child object from the generic `IReader`interface.

## Methods

### Constructor

**Parameters**

- `markdown_content` : str
    - The content of the markdown file to be read.

### _convert_to_markdown

Converts the markdown content into markdown format. So in that case, it returns the same content.

**Returns**

- `str` : The markdown content.

### read

Inherited from the `IReader` interface.

**Returns**

- `dict` : The nested dictionary that represents the markdown file.

*See [IReader](ireader.md) for more information.*

##### Usage example

###### Code
```python

markdown_content = "# Title \n This is a paragraph"
reader = MarkdownReader(markdown_content)
dict_struct = reader.read()
print(dict_struct)

```

###### Output
```py
 {
        'type' : 'container' or 'block',
        'children' : [list of nested dictionaries],
        'content' : None or string,
        'level' : int,
        'parent' : parent dictionary
    }

```