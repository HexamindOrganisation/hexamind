import json
import os

from mistralai.client import MistralClient
from openai import OpenAI

from hexamind.llm.adapters.api.MistralApiAdapter import MistralClientAdapter
from hexamind.llm.adapters.api.OpenAiApiAdapter import OpenAiClientAdapter
from openai import OpenAI
from hexamind.llm.adapters.op.LlmOpAdapter import LlmOpAdapter
from hexamind.llm.adapters.ChatMessageFactory import ChatMessageFactory


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
    def create_adapter(llm_name, on_premise=False, **kwargs):
        """
        Create the proper adaptater for the LLM client according to the configuration.
        """

        if on_premise:
            try:
                chat_method = ChatMessageFactory.create_chat_message(llm_name)
                return LlmOpAdapter(**kwargs, chat_method=chat_method)
            except Exception as e:
                raise ValueError(f"Could not create LlmOpAdapter: {e}")
        else:

            if llm_name == "mistral":
                try:
                    return MistralClientAdapter(
                        MistralClient(api_key=kwargs["api_key"]),
                        kwargs["model"],
                        kwargs["embed_model"],
                    )
                except Exception as e:
                    raise ValueError(f"Could not create MistralClientAdapter: {e}")
            elif llm_name == "openai":
                try:
                    return OpenAiClientAdapter(
                        OpenAI(api_key=kwargs["api_key"]),
                        kwargs["model"],
                        kwargs["embed_model"],
                    )
                except Exception as e:
                    raise ValueError(f"Could not create OpenAiClientAdapter: {e}")
            else:
                raise ValueError(f"Unsupported llm name: {llm_name}")
