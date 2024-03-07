from hexs_rag.llm.adapters.AbstractLlm import ILlmClient
from mistralai.models.chat_completion import ChatMessage

class MistralClientAdaptater(ILlmClient):
    def __init__(self, client):
        self.client = client


    def chat(self, model, messages, temperature=0):
        chat_response = self.client.chat(
            model=model,
            messages=messages,
            temperature=temperature
        )
        return chat_response.choices[0].message.content
    
    def create_chat_message(self, role, content):
        return ChatMessage(role=role, content=content)