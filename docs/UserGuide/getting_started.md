# Getting Started

This is a guide to help you get started with the hexamind library. 
## Installation

### Using pip

You should be able to install the library using pip. But you must have the hxm_rag repository cloned on your local machine. Because this library is private and not yet deploy on private registry. 

```bash
git clone https://github.com/HexamindOrganisation/hexamind.git
```

Then you can install the library using pip.

```bash
pip install -e path/to/hexamind
```

## Usage

The library serves many purpose and can be used not only for RAG solutions but also when you need to parse some document and just use a Llm agent. 

### Parsing a docx file

Here is a simple example of how to parse a docx file using the WordReader class. 

```py

from hxm_rag.model import WordReader

# Create an instance of the WordReader class

word_reader = WordReader("path/to/your/docx/file")

# Create a nested dictionnary structure of the document

doc_structure = word_reader.get_document_structure()

```

this sample should give you a nested dictionnary structure that must look like this:

```py

  {
        'type' : 'container' or 'block',
        'children' : [list of nested dictionaries],
        'content' : None or string,
        'level' : int,
        'parent' : parent dictionary
    }

```

See [readers](readers.md) for more information about the readers available in the library and the return format.

### Converting a nested dictionnary into a Document object

To get more information about the document [click here](model.md) 

You can then convert the nested dictionnary into the hxm_rag Document object. 

```py

from hexamind import Document

doc = Document(doc_structure)

```

### Using the LLm agent 

You can use select the proper agent in many ways, feel free to explore the [llm](llm.md) module to see the different model supported by the library. 

```py
from hexamind.llm.adapters import MistralClientAdapter
from hexamind import LlmAgent
from mistralai import MistralClient

# Create an instance of the MistralClient class

mistral_client = MistralClientAdapter(MistralClient('your_mistral_api_key'))

# Create an instance of the LlmAgent class

llm_agent = LlmAgent(mistral_client)
```

A factory method is also available to instanciate the client automatically. This can be coupled with the Initializer class that can initialize every component needed in your solution. 




