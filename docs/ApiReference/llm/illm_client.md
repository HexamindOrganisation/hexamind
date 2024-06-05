# ILlmClient

## Overview

The `ILlmClient` interface is used to define the methods that the llm client should implement. All the adapters inherit from this interface. You can create your own adapter thanks to this interface.

## ILlmClient

### Methods

#### chat 

Chat with the llm model.

**Parameters:**

- `messages` (str): The messages to send to the llm model.
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