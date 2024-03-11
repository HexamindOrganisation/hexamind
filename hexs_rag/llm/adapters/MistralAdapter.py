from hexs_rag.llm.adapters.AbstractLlm import ILlmClient
from mistralai.models.chat_completion import ChatMessage

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
    def __init__(self, client,model="mistral-large-latest", embed_model = 'mistral-embed'):
        if not isinstance(client, ILlmClient):
            raise TypeError("client should be an instance of ILlmClient")
        
        if not isinstance(model, str):
            raise TypeError("model should be a string")
        
        if not isinstance(embed_model, str):
            raise TypeError("embed_model should be a string")
        
        self.client = client
        self.model = model
        self.embed_model = embed_model


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
                inputs=input
        )
        except Exception as e:
            raise ValueError(f"Could not get embeddings from Mistral: {e}, please check the embedded model name.")