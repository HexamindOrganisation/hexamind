import os
import logging
import time
from mistralai.models.chat_completion import ChatMessage
from mistralai.exceptions import MistralAPIException
from hexamind.llm.adapters.AbstractLlm import ILlmClient

logger = logging.getLogger(__name__)


class MistralClientAdapter(ILlmClient):
    def __init__(self, client, model=None, embed_model=None):
        logger.debug("MistralClientAdapter initialization...")
        self.client = client
        self.model = (
            model
            if model is not None
            else os.getenv("LLM_MODEL", "mistral-large-latest")
        )
        self.embed_model = (
            embed_model
            if embed_model is not None
            else os.getenv("LLM_EMBED_MODEL", "mistral-embed")
        )

        if not isinstance(self.model, str):
            raise TypeError("model should be a string")

        if not isinstance(self.embed_model, str):
            raise TypeError("embed_model should be a string")

    def chat(self, messages, temperature=0):
        try:
            chat_response = self.client.chat(
                model=self.model, messages=messages, temperature=temperature
            )
            return chat_response.choices[0].message.content
        except Exception as e:
            logger.error(f"Could not chat with Mistral: {e}")
            raise ValueError(f"Could not chat with Mistral: {e}")

    def create_chat_message(self, role, content):
        try:
            return ChatMessage(role=role, content=content)
        except Exception as e:
            logger.error(f"Could not create chat message for Mistral: {e}")
            raise ValueError(f"Could not create chat message for Mistral: {e}")

    def embeddings(self, input):
        max_retries = 3
        retries = 0
        while retries < max_retries:
            try:
                return self.client.embeddings(model=self.embed_model, input=input)
            except MistralAPIException as e:
                if e.http_status == 429:
                    retries += 1
                    retry_after = int(e.headers.get("Retry-After", 2**retries))
                    logger.warning(f"Rate limited, retrying in {retry_after} seconds")
                    time.sleep(retry_after)
                else:
                    logger.error(f"Mistral API Exception: {e}")
                    raise e
        logger.error("Rate limited too many times")
        raise MistralAPIException("Rate limited too many times")
