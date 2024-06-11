# How to use and work with the models

This is a short introducton that aims to help user to manipulate the hexamind library, in particular the differents models.

Firts, let's begin with the readers and how to use them. 

## Readers

First we need to import the readers we want to use. In this example we will use the HtlmReader  but note that the process is similar for any readers.

```python

from hexamind.readers import HtlmReader
import requests

```

Then let's get a htlm page from the web using the `requests` library.

```python

url = "https://fr.wikipedia.org/wiki/Python_(langage)"
response = requests.get(url)
html = response.text

```

*Here we're scrapping the Python page on wikipedia using requests but you can also use the `wikipedia` library.*

Now we can use the `HtlmReader` to convert the htlm format into markdown.

```python

reader = HtlmReader(html)

```

```python

markdown_content = reader.convert_to_markdown()

```

## Document

Now we have converted the htlm page into markdown, we can create a document object.

```python

from hexamind.model import Document

doc = Document(markdown_content)

```

Let's print that document structure 

```python

print(doc)

```

```python

