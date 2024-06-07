# WordReader

## Overview 

`WordReader` is a class that reads docx/doc files and convert the format into the nested dictionnary structure using `MkTransformer`. It is a child object from the generic `IReader`interface. 

## Methods

### Constructor 

**Parameters**

- `path` : str
    - The path to the docx/doc file to be read.

### _convert_to_markdown

Converts the word file content into markdown format.

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

docx_path = "path/to/docx/file.docx"
reader = WordReader(docx_path)
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