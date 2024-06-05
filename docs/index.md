# Home

## Welcome to the HXM RAG documentation

This documentation is the official document for the Hxm_rag library. 

This library is aiming to provide a simple and easy way to use and create the RAG technique. This project is intended to be jused only for Hexamind's projects.

## Library Overview

The library can be used in many ways. Not only for deploying RAG but it offers some useful tools to parse documents, create embeddings or use LLm models. 

### Library structure 

```plaintext
📦hxm_rag
 ┣ 📂database
 ┃ ┣ 📂adapters
 ┃ ┃ ┣ 📜AbstractDb.py
 ┃ ┃ ┣ 📜ChromaDbAdapter.py
 ┃ ┃ ┣ 📜DbAdapterFactory.py
 ┃ ┃ ┣ 📜ElasticSearchAdapter.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂ingestion
 ┃ ┃ ┗ 📜ingestor.py
 ┃ ┗ 📜__init__.py
 ┣ 📂initializer
 ┃ ┣ 📜__init__.py
 ┃ ┗ 📜initializer.py
 ┣ 📂llm
 ┃ ┣ 📂adapters
 ┃ ┃ ┣ 📂api
 ┃ ┃ ┃ ┣ 📜MistralApiAdapter.py
 ┃ ┃ ┃ ┣ 📜OpenAiApiAdapter.py
 ┃ ┃ ┃ ┗ 📜__init__.py
 ┃ ┃ ┣ 📂op
 ┃ ┃ ┃ ┗ 📜LlmOpAdapter.py
 ┃ ┃ ┣ 📜AbstractLlm.py
 ┃ ┃ ┣ 📜ChatMessageFactory.py
 ┃ ┃ ┣ 📜LlmAdapterFactory.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂llm
 ┃ ┃ ┣ 📜LlmAgent.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┗ 📜__init__.py
 ┣ 📂model
 ┃ ┣ 📂model
 ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┣ 📜block.py
 ┃ ┃ ┣ 📜container.py
 ┃ ┃ ┣ 📜document.py
 ┃ ┃ ┗ 📜element.py
 ┃ ┣ 📂readers
 ┃ ┃ ┣ 📜HtmlReader.py
 ┃ ┃ ┣ 📜WordReader.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┗ 📜__init__.py
 ┣ 📂retriever
 ┃ ┣ 📜__init__.py
 ┃ ┗ 📜retriever.py
 ┣ 📂utils
 ┣ 📜__init__.py
 ┗ 📜requirements.txt
```

