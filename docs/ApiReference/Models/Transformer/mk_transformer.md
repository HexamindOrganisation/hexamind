# MkTransformer

## Overview

`MkTransformer` is a class that transforms markdown content into nested dictionnaries that will be used by the `Document` class to generate the Node tree structure using Container and Blocks objects. 

## Methods

### @classmethod from_mardown

Converts the markdown content into a nested dictionnary.

**Parameters**

- `markdown_content` : str
    - The markdown content to be transformed.

**Returns**

- `dict` : The nested dictionnary.
    - the dictionnary is structured like that : 

```py

    {
        'type' : 'container' or 'block',
        'children' : [list of nested dictionaries],
        'content' : None or string,
        'level' : int,
        'parent' : parent dictionary
    }

```

##### Usage example

###### Code
```py

markdown_content = "# Title \n\n This is a paragraph"
doc_structure = MkTransformer.from_mardown(markdown_content)
print(doc_structure)

```

###### Output
```py

{
    'type': 'container',
    'children': [
        {
            'type': 'container',
            'children': [
                {
                    'type': 'container',
                    'children': [
                        {
                            'type': 'block',
                            'content': 'Title',
                            'level': 1,
                            'parent': {...}
                        }
                    ],
                    'content': None,
                    'level': 1
                },
                {
                    'type': 'container',
                    'children': [
                        {
                            'type': 'block',
                            'content': 'This is a paragraph',
                            'level': 1,
                            'parent': {...}
                        }
                    ],
                    'content': None,
                    'level': 1
                }
            ],
            'content': None,
            'level': 1
        }
    ],
    'content': None,
    'level': 0
}

```
