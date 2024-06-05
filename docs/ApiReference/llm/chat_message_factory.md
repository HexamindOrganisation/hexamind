# ChatMessageFactory

*Note : The `ChatMessageFactory` is still under development and will be updated soon.*

## Overview

This factory is only used with the models self-hosted. It is responsible for creating the chat messages to send to the model.

## ChatMessageFactory

**Attributes:**

- `model_type` (str): The type of the model.

### Methods

#### create_chat_message

Create a chat message based on the model type.

**Parameters:**

- `role` (str): The role of the message. ('user' or 'agent')
- `content` (str): The content of the message.