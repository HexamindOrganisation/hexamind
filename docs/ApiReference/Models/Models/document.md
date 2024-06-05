# Document

*Note: This document is a work in progress. The content and structure may change.*

## Overview 

The document class encapsulates the structure of a real document into the hxm_rag representation. 
This is the global entry point for all the data manupulation.

**Attributes:**

- `document_structure` (Dict): The structure of the document.

##### Usage Example

```py

dict_structure = WordReader("path/to/word_file").get_document_structure()
document = Document(dict_structure)

```

## Methods

#### prepare_for_ingestion

The method will population every content of a child container to it parent container until reaching the root container. Basically it will create a mutliple level content structure.

##### Usage Example

```py

dict_structure = WordReader("path/to/word_file").get_document_structure()
document = Document(dict_structure)
document.prepare_for_ingestion()

```

