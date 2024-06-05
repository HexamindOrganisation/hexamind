# LlmOpAdapter

*Note: The `LlmOpAdapter` is still under development and will be updated soon.*

## Overview 

The `LlmOpAdapter` class is used to interface with your self-hosted model. This class implements the `ILlmClient` interface. 

**Attributes:**

- `inference_endpoint` (str): The endpoint of the model.
- `embeddings_endpoint` (str): The endpoint of the embeddings.
- `chat_method` : You must pass the chat message method you want to use according to the model. For now only the Mistral chat method is implemented.

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
