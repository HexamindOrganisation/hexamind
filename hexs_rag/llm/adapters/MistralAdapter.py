from hexs_rag.llm.adapters.AbstractLlm import ILlmClient
from mistralai.models.chat_completion import ChatMessage
import os

class MistralClientAdapter(ILlmClient):
    """
    Adapater class for using the Mistral client.
    This class implements the ILlmClient interface.

    Attributes:
    client : MistralClient
        The client to use for the LLM.
    model : str
        The model to use for the LLM. (e.g. "mistral-large-latest" if using Mistral)
    embed_model : str
        The model to use for the embeddings. (e.g. "mistral-embed" if using Mistral)
    
    Methods: 
    chat(self, model, messages, temperature=0)
        Send a request to the LLM and get the response. 
    create_chat_message(self, role, content)
        Create a chat message according to the client's message format. Here is the specific format for Mistral.
    """
    def __init__(self, client,model=None, embed_model = None):
        
        self.client = client
        self.model = model if model is not None else os.getenv('LLM_MODEL', 'mistral-large-latest')
        self.embed_model = embed_model if embed_model is not None else os.getenv('LLM_EMBED_MODEL', 'mistral-embed')

        if not isinstance(self.model, str):
            raise TypeError("model should be a string")
        
        if not isinstance(self.embed_model , str):
            raise TypeError("embed_model should be a string")


    def chat(self, messages, temperature=0):
        try: 
            chat_response = self.client.chat(
                model=self.model,
                messages=messages,
                temperature=temperature
            )
            return chat_response.choices[0].message.content
        except Exception as e:
            raise ValueError(f"Could not chat with Mistral: {e}")
    
    def create_chat_message(self, role, content):
        try:
            return ChatMessage(role=role, content=content)
        except Exception as e:
            raise ValueError(f"Could not create chat message for Mistral: {e}")

    def embeddings(self, input):
        try: 
            return self.client.embeddings(
                model=self.embed_model,
                input=input
        )
        except Exception as e:
            raise ValueError(f"Could not get embeddings from Mistral: {e}, please check the embedded model name.")