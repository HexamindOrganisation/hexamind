from hexs_rag.llm.adapters.AbstractLlm import ILlmClient

class OpenAiClientAdapter(ILlmClient):
    """
        Adapater class for using the OpenAI client.
    This class implements the ILlmClient interface.

    Attributes:
    client : OpenAIClient
        The client to use for the LLM.
    model : str
        The model to use for the LLM. (e.g. "gpt-3.5-turbo" if using OpenAI)
    embed_model : str
        The model to use for the embeddings. (e.g. "text-embedding-3-large" if using OpenAI)
    
    Methods: 
    chat(self, model, messages, temperature=0)
        Send a request to the LLM and get the response. 
    create_chat_message(self, role, content)
        Create a chat message according to the client's message format. Here is the specific format for OpenAI.
    """
    def __init__(self, client, model="gpt-3.5-turbo", embed_model = 'text-embedding-3-large'):
        self.client = client
        self.model = model
        self.embed_model = embed_model
    
    def chat(self, messages, temperature=0):
        chat_response = self.client.chat.completion.create(
            model=self.model,
            messages=[messages],
        )
        return chat_response.choices[0].message.content
    
    def create_chat_message(self, role, content):
        message = {
            "role": role,
            "content": content
        }
        return message
    
    def embeddings(self, input):
        return self.client.embeddings.create(
            model=self.embed_model,
            inputs=input
        )