# MistralClientAdapter

## Overview

The `MistralClientAdapter` class is used to interface with the Mistral API. This class implements the `ILlmClient` interface.

**Attributes:**

- `client` (MistralClient): The Mistral client used to interface with the Mistral API.
- `model` (str): The model to use for the llm agent.
- `embed_model` (str): The model to use for the embeddings.

### Methods

#### chat

Chat with the Mistral model.

**Parameters:**

- `messages` (str): The messages to send to the Mistral model.
- `temperature` (float): The temperature of the model.


#### create_chat_message

Create a chat message.

**Parameters:**

- `role` (str): The role of the message. ('user' or 'agent')
- `content` (str): The content of the message.

#### embeddings

Get the embeddings of the text.

**Parameters:**

- `input` (str): The text to get the embeddings from.

### How to import 

```py

from hexamind.llm.adapters import MistralClientAdapter

```