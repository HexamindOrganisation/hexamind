# HtmlReader

## Overview 

`HtmlReader` is a class that reads HTML files and convert the htlm format into markdown. It is a child object from the generic `IReader`interface. 

## Methods

### Constructor 

**Parameters**

- `htlm_content` : str
    - The content of the HTML file to be read.

### convert_to_markdown

Converts the HTML content into markdown format.

**Returns**

- `str` : The markdown content.

##### Usage example

###### Code
```python 

html_content = "<h1> Title </h1> <p> This is a paragraph </p>"
reader = HtmlReader(html_content)
markdown_content = reader.convert_to_markdown()
print(markdown_content)

```

###### Output
```markdown
# Title

This is a paragraph
```