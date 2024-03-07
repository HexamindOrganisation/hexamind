import json
from mistralai.client import MistralClient
from hexs_rag.llm.adapters import MistralClientAdaptater, OpenAiClientAdaptater
from openai import OpenAI

class LlmAdaptaterFactory:

    def create_adaptater(config_path='hexs_rag/config/config.json'):
        with open(config_path) as f:
            config = json.load(f)

            llm_name = config['llm_name']

            if llm_name == 'mistral':
                return MistralClientAdaptater(MistralClient(config['credentials']['api_key']))
            elif llm_name == 'chatgpt':
                return OpenAiClientAdaptater(OpenAI(config['credentials']['api_key']))
            else:
                raise ValueError(f"Unsupported llm name: {llm_name}")