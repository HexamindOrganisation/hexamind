from mistralai.models.chat_completion import ChatMessage


def MistralChatMessage(role, content):
    return ChatMessage(role=role, content=content)


def LlamaChatMessage(role, content):
    pass
