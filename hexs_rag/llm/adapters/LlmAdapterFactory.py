import json
import os

from mistralai.client import MistralClient
from openai import OpenAI

from hexs_rag.llm.adapters.api.MistralApiAdapter import MistralClientAdapter
from hexs_rag.llm.adapters.api.OpenAiApiAdapter import OpenAiClientAdapter


class LlmAdapterFactory:
    """
    This factory class is used to create the adaptater for the LLM client.
    Depending on the configuration, it will create the adaptater for the right LLM client.

    Methods:
    create_adaptater(llm_name, llm_api_key)
        Create the proper adaptater for the LLM client according to the configuration.
        This is a static method meaning that it can be called without creating an instance of the class.
    """

    @staticmethod
    def create_adapter(llm_name, llm_api_key, model=None, embed_model=None):
        """
        Create the proper adaptater for the LLM client according to the configuration.
        """

        if llm_name == "mistral":
            try:
                return MistralClientAdapter(
                    MistralClient(api_key=llm_api_key), model, embed_model
                )
            except Exception as e:
                raise ValueError(f"Could not create MistralClientAdapter: {e}")
        elif llm_name == "openai":
            try:
                return OpenAiClientAdapter(
                    OpenAI(api_key=llm_api_key), model, embed_model
                )
            except Exception as e:
                raise ValueError(f"Could not create OpenAiClientAdapter: {e}")
        else:
            raise ValueError(f"Unsupported llm name: {llm_name}")
