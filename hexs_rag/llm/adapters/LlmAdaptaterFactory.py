import json
from mistralai.client import MistralClient
from hexs_rag.llm.adapters.MistralAdaptater import MistralClientAdaptater
from hexs_rag.llm.adapters.OpenAiAdaptater import OpenAiClientAdaptater
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
        with open(config_path) as f:
            config = json.load(f)

            llm_name = config['llm_name']

            if llm_name == 'mistral':
                return MistralClientAdaptater(MistralClient(config['credentials']['api_key']))
            elif llm_name == 'chatgpt':
                return OpenAiClientAdaptater(OpenAI(api_key = config['credentials']['api_key']))
            else:
                raise ValueError(f"Unsupported llm name: {llm_name}")