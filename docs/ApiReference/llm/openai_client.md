# OpenAiClientAdapter

## Overview

The `OpenAiClientAdapter` class is used to interface with the OpenAi API. This class implements the `ILlmClient` interface.

**Attributes:**

- `client` (OpenAiClient): The OpenAi client used to interface with the OpenAi API.
- `model` (str): The model to use for the llm agent.
- `embed_model` (str): The model to use for the embeddings.

### Methods

#### chat

Chat with the OpenAi model.

**Parameters:**

- `messages` (str): The messages to send to the OpenAi model.
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