from hexs_rag.llm.adapters.AbstractLlm import ILlmClient
from mistralai.models.chat_completion import ChatMessage

class MistralClientAdaptater(ILlmClient):
    """
    Adapater class for using the Mistral client.
    This class implements the ILlmClient interface.

    Attributes:
    client : MistralClient
        The client to use for the LLM.
    
    Methods: 
    chat(self, model, messages, temperature=0)
        Send a request to the LLM and get the response. 
    create_chat_message(self, role, content)
        Create a chat message according to the client's message format. Here is the specific format for Mistral.
    """
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