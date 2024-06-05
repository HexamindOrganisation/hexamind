# LlmAdapterFactory

## Overview

This llm factory is responsible for perfectly instanciate the llm agent based on the configuration provided. 

## LlmAdapterFactory

### Methods

#### create_adapter

Create a llm agent based on the llm type. Note that this method can create the proper agent either from a self-hosted model or from the APIs (like Mistral or OpenAI). You only have to specify if the model is on premise or not.

**Parameters:**

- `llm_name` (str): The name of the llm model you want to use. Mandatory if the model is not on premise.
- `on_premise` (bool): If the model is on premise or not. Default is False.
- `kwargs` (dict): The keyword arguments to pass to the llm agent.
    - *For API models*:
        - `api_key` (str): The api key of the Mistral model.
        - `model` (str): The model to use for the llm agent.
        - `embed_model` (str): The model to use for the embeddings.
    - *For on premise models*:
        - `inference_endpoint` (str): The endpoint of the model.
        - `embeddings_endpoint` (str): The endpoint of the embeddings.

**Returns:**

- `ILlmClient`: Returns on instance of the llm client adapter interface. 


### API models supported

At the moment the following API models are supported:

- Mistral
- OpenAI


### Usage Example

###### Code

```py

llm_adapter = LlmAdapterFactory.create_adapter(llm_name='mistral', on_premise=False, api_key='api_key', model='mistral-large', embed_model='mistral-embed')

llm_agent = LlmAgent(client=llm_adapter)

```

### How to import 

```py

from hexamind.llm.adapters import LlmAdapterFactory

```