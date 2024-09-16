import hexamind.utils.llm.chat_message as chat_message


class ChatMessageFactory:

    def __init__(self, model_type):
        self.model_type = model_type

    def create_chat_message(self, role, content):
        if self.model_type == "mistral":
            return chat_message.MistralChatMessage(role, content)
        elif self.model_type == "llama":
            return chat_message.LlamaChatMessage(role, content)
