from hexs_rag.llm.adapters.AbstractLlm import ILlmClient

class OpenAiClientAdaptater(ILlmClient):
    """
        Adapater class for using the OpenAI client.
    This class implements the ILlmClient interface.

    Attributes:
    client : OpenAIClient
        The client to use for the LLM.
    
    Methods: 
    chat(self, model, messages, temperature=0)
        Send a request to the LLM and get the response. 
    create_chat_message(self, role, content)
        Create a chat message according to the client's message format. Here is the specific format for OpenAI.
    """
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