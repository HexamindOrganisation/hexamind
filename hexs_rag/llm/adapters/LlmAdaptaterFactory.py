import json
import os
from mistralai.client import MistralClient
from hexs_rag.llm.adapters import MistralClientAdaptater, OpenAiClientAdaptater
from openai import OpenAI

class LlmAdaptaterFactory:
    """
    This factory class is used to create the adaptater for the LLM client.
    Depending on the configuration, it will create the adaptater for the right LLM client.

    Methods:
    create_adaptater(config_path)
        Create the proper adaptater for the LLM client according to the configuration.
    """

    def create_adaptater(config_path='hexs_rag/config/config.json'):
        llm_name = os.getenv('LLM_NAME')

        if llm_name == 'mistral':
            return MistralClientAdaptater(MistralClient(api_key = os.getenv('LLM_API_KEY')))
        elif llm_name == 'chatgpt':
            return OpenAiClientAdaptater(OpenAI(api_key = os.getenv('LLM_API_KEY')))
        else:
            raise ValueError(f"Unsupported llm name: {llm_name}")