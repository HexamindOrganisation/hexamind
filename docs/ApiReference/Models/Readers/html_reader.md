# HtmlReader

## Overview 

`HtmlReader` is a class that reads HTML files and convert the format into the nested dictionnary structure using `MkTransformer`. It is a child object from the generic `IReader`interface. 

## Methods

### Constructor 

**Parameters**

- `htlm_content` : str
    - The content of the HTML file to be read.

### _convert_to_markdown

Converts the HTML content into markdown format.

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

html_content = "<h1> Title </h1> <p> This is a paragraph </p>"
reader = HtmlReader(html_content)
dict_struc = reader.read()
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