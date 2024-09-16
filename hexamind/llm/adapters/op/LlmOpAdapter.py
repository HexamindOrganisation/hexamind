from hexamind.llm.adapters.AbstractLlm import ILlmClient
import requests


class LlmOpAdapter(ILlmClient):
    """
    This class is a general adapter for LLM models deployed on premise
    """

    def __init__(self, inference_endpoint, embeddings_endpoint, chat_method):

        self.inference_endpoint = inference_endpoint
        self.embeddings_endpoint = (embeddings_endpoint,)
        self.chat_method = chat_method

    def chat(self, messages, temperature=0):
        try:
            return requests.post(
                self.inference_endpoint,
                json={"messages": messages, "temperature": temperature},
            ).json()
        except Exception as e:
            raise ValueError(f"Could not chat with LLM: {e}")

    def create_chat_message(self, role: str, content: str):
        return self.chat_method(role, content)

    def embeddings(self, input):
        try:
            return requests.post(self.embeddings_endpoint, json={"input": input}).json()
        except Exception as e:
            raise ValueError(f"Could not get embeddings: {e}")
