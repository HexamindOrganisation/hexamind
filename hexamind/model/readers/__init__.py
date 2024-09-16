"""
Readers are used to read the input data from different sources. All the readers returns the same data structure which is a nested dictionary representing the structure of the document.

The readers are:
- WordReader: Reads the content of a Word document.
- HtmlReader: Reads the content of an HTML document.

The structure of the dictionary is as follows:

{
    'type' : 'container' or 'block',
    'children' : [list of nested dictionaries],
    'content' : None or string,
    'level' : int,
    'parent' : parent dictionary
}

The 'type' key indicates if the dictionary represents a container or a block.

The 'children' key contains a list of nested dictionaries that represent the children of the current dictionary.

The 'content' key contains the text content of the block or container. If the dictionary represents a container, the content is None.

The 'level' key contains the level of the block or container in the hierarchy.

The 'parent' key contains a reference to the parent dictionary in the hierarchy.
"""

from .HtmlReader import HtmlReader
from .WordReader import WordReader
from .IReader import IReader
