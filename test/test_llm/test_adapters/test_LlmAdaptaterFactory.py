import pytest
import os
from hexs_rag.llm.adapters.LlmAdapterFactory import LlmAdapterFactory
from hexs_rag.llm.adapters.OpenAiAdapter import OpenAiClientAdapter
from hexs_rag.llm.adapters.MistralAdapter import MistralClientAdapter
from unittest.mock import patch, MagicMock
from unittest.mock import create_autospec

@pytest.fixture(params=["mistral", "openai", "unsupported"])
def llm_name_env(request, monkeypatch):
    monkeypatch.setenv("LLM_NAME", request.param)
    monkeypatch.setenv("LLM_API_KEY", "test")
    if request.param == "mistral":
        return request.param, MistralClientAdapter
    elif request.param == "openai":
        return request.param, OpenAiClientAdapter
    else:
        return request.param, None

@patch('mistralai.client.MistralClient', MagicMock())
@patch('openai.OpenAI', MagicMock())
def test_create_adapter(llm_name_env):
    llm_name, expected_type = llm_name_env
    if expected_type is not None:
        adapter = LlmAdapterFactory.create_adapter(os.getenv("LLM_NAME"), os.getenv("LLM_API_KEY"))
        assert isinstance(adapter, expected_type)
    else:
        with pytest.raises(ValueError):
            LlmAdapterFactory.create_adapter(os.getenv("LLM_NAME"), os.getenv("LLM_API_KEY"))