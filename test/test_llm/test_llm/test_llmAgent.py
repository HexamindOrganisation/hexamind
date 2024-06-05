import pytest
from unittest.mock import create_autospec, ANY
from hexamind.llm.adapters.AbstractLlm import ILlmClient
from hexamind.llm.llm.LlmAgent import LlmAgent

@pytest.fixture
def mock_llm_client():
    return create_autospec(ILlmClient)

def test_send_request_to_llm(mock_llm_client):
    agent = LlmAgent(mock_llm_client)
    mock_llm_client.chat.return_value = "expected response"
    result = agent.send_request_to_llm(messages="test message")
    mock_llm_client.chat.assert_called_once_with(messages="test message")
    assert result == "expected response"

def test_generate_paragraph(mock_llm_client):
    agent = LlmAgent(mock_llm_client)
    mock_llm_client.create_chat_message.return_value = "test message"
    mock_llm_client.chat.return_value = "expected response"
    result = agent.generate_paragraph(query="test query", context={"test": "context"}, histo=[("test", "histo")], language="fr")
    mock_llm_client.create_chat_message.assert_called_once_with("user", ANY)
    mock_llm_client.chat.assert_called_once_with(messages=["test message"])
    assert result == "expected response"