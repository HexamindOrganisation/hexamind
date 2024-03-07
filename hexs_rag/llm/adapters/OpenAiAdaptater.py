from hexs_rag.llm.adapters.AbstractLlm import ILlmClient

class OpenAiClientAdaptater(ILlmClient):
    def __init__(self, client):
        self.client = client
    
    def chat(self, model, messages, temperature=0):
        chat_response = self.client.chat.completion.create(
            model=model,
            messages=[messages],
        )
        return chat_response.choices[0].message
    
    def create_chat_message(self, role, content):
        message = {
            "role": role,
            "content": content
        }
        return message