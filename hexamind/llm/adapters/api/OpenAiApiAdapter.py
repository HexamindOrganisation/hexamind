import os

from hexamind.llm.adapters.AbstractLlm import ILlmClient


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

    def __init__(self, client, model=None, embed_model=None):

        self.client = client
        self.model = (
            model if model is not None else os.getenv("LLM_MODEL", "gpt-3.5-turbo")
        )
        self.embed_model = (
            embed_model
            if embed_model is not None
            else os.getenv("LLM_EMBED_MODEL", "text-embedding-3-large")
        )

        if not isinstance(self.model, str):
            raise TypeError("model should be a string")
        if not isinstance(self.embed_model, str):
            raise TypeError("embed_model should be a string")

    def chat(self, messages, temperature=0):
        try:
            chat_response = self.client.chat.completion.create(
                model=self.model,
                messages=[messages],
            )
            return chat_response.choices[0].message.content
        except Exception as e:
            raise ValueError(f"Could not chat with OpenAI: {e}")

    def create_chat_message(self, role, content):
        try:
            return {"role": role, "content": content}
        except Exception as e:
            raise ValueError(f"Could not create chat message for OpenAI: {e}")

    def embeddings(self, input):
        try:
            return self.client.embeddings.create(model=self.embed_model, inputs=input)
        except Exception as e:
            raise ValueError(
                f"Could not get embeddings from OpenAI: {e}, please check the embedded model name."
            )
