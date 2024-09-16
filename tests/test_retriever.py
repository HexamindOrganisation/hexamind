import pytest
from unittest.mock import Mock, patch
import numpy as np
from hexamind.retriever import Retriever
from hexamind.utils.config.retriever import RetrieverConfig
from hexamind.model.chunk.chunk import Chunk

@pytest.fixture
def mock_db_client():
    return Mock()

@pytest.fixture
def mock_llm_agent():
    return Mock()

@pytest.fixture
def mock_cohere_client():
    return Mock()

@pytest.fixture
def config():
    return RetrieverConfig(
        cohere_api_key="test_key",
        max_hybrid_search_results=50,
        rrf_k=60,
        rerank_model="test-model",
        max_rerank_results=30,
        peloton_alpha=0.15,
        peloton_beta=0.3,
        min_chunks_to_return=1,
        max_chunks_to_return=30
    )

@pytest.fixture
def retriever(mock_db_client, mock_llm_agent, config, mock_cohere_client):
    with patch('cohere.Client', return_value=mock_cohere_client):
        return Retriever(mock_db_client, mock_llm_agent, config)

def test_init(retriever, mock_db_client, mock_llm_agent, config):
    assert retriever.db_client == mock_db_client
    assert retriever.llm_agent == mock_llm_agent
    assert retriever.config == config

def test_similarity_search(retriever, mock_db_client, mock_llm_agent):
    query = "test query"
    condition = {"field": "value"}
    mock_llm_agent.get_embedding.return_value = [0.1, 0.2, 0.3]
    mock_llm_agent.get_sparse_embedding.return_value = [1, 0, 1, 0]
    mock_db_client.hybrid_search.return_value = [Chunk("content", "container_uid", "doc_uid", "title", 1, "doc_title", "1", 1, 0.5)]

    result = retriever.similarity_search(query, condition)

    mock_llm_agent.get_embedding.assert_called_once_with(query)
    mock_llm_agent.get_sparse_embedding.assert_called_once_with(query)
    mock_db_client.hybrid_search.assert_called_once_with(
        query_dense_vector=[0.1, 0.2, 0.3],
        query_sparse_vector=[1, 0, 1, 0],
        num_results=50,
        condition=condition
    )
    assert len(result) == 1
    assert isinstance(result[0], Chunk)

def test_hybrid_search(retriever, mock_db_client):
    query_dense_vector = [0.1, 0.2, 0.3]
    query_sparse_vector = [1, 0, 1, 0]
    condition = {"field": "value"}
    mock_db_client.search.side_effect = [
        [Chunk("content1", "container_uid1", "doc_uid1", "title1", 1, "doc_title1", "1", 1, 0.5)],
        [Chunk("content2", "container_uid2", "doc_uid2", "title2", 2, "doc_title2", "2", 2, 0.7)]
    ]

    result = retriever.hybrid_search(query_dense_vector, query_sparse_vector, condition)

    assert mock_db_client.search.call_count == 2
    assert len(result) == 2
    assert all(isinstance(chunk, Chunk) for chunk in result)
    
    # Check that the chunks are in the correct order (highest RRF score first)
    assert result[0].document_uid == "doc_uid1" and result[0].index == 1
    assert result[1].document_uid == "doc_uid2" and result[1].index == 2

    # Check that the distances (RRF scores) are in descending order
    assert result[0].distance > result[1].distance

    # Add a test with a more complex document_uid
    mock_db_client.search.side_effect = [
        [Chunk("content3", "container_uid3", "doc_uid_with_underscore_3", "title3", 3, "doc_title3", "3", 3, 0.9)],
        [Chunk("content4", "container_uid4", "doc_uid4", "title4", 4, "doc_title4", "4", 4, 0.6)]
    ]

    result = retriever.hybrid_search(query_dense_vector, query_sparse_vector, condition)

    assert len(result) == 2
    assert result[0].document_uid == "doc_uid_with_underscore_3" and result[0].index == 3
    assert result[1].document_uid == "doc_uid4" and result[1].index == 4
    assert result[0].distance > result[1].distance

def test_reranker(retriever, mock_cohere_client):
    query = "test query"
    chunks = [
        Chunk("content1", "container_uid1", "doc_uid1", "title1", 1, "doc_title1", "1", 1, 0.5),
        Chunk("content2", "container_uid2", "doc_uid2", "title2", 2, "doc_title2", "2", 2, 0.7)
    ]
    mock_cohere_client.rerank.return_value.results = [
        Mock(index=1, relevance_score=0.8),
        Mock(index=0, relevance_score=0.6)
    ]

    result = retriever.reranker(query, chunks)

    mock_cohere_client.rerank.assert_called_once_with(
        model="test-model",
        query=query,
        documents=["content1", "content2"],
        top_n=30
    )
    assert len(result) == 2
    assert result[0].distance == 0.8
    assert result[1].distance == 0.6

def test_peloton_selection(retriever):
    chunks = [
        Chunk("content1", "container_uid1", "doc_uid1", "title1", 1, "doc_title1", "1", 1, 0.9),
        Chunk("content2", "container_uid2", "doc_uid2", "title2", 2, "doc_title2", "2", 2, 0.8),
        Chunk("content3", "container_uid3", "doc_uid3", "title3", 3, "doc_title3", "3", 3, 0.7),
        Chunk("content4", "container_uid4", "doc_uid4", "title4", 4, "doc_title4", "4", 4, 0.6),
        Chunk("content5", "container_uid5", "doc_uid5", "title5", 5, "doc_title5", "5", 5, 0.5)
    ]

    result = retriever.peloton_selection(chunks)

    assert 1 <= len(result) <= 30  # min_chunks_to_return <= result <= max_chunks_to_return
    assert all(isinstance(chunk, Chunk) for chunk in result)
    assert result == sorted(result, key=lambda x: x.distance, reverse=True)

def test_retrieve(retriever, mock_llm_agent):
    query = "test query"
    condition = {"field": "value"}
    mock_llm_agent.get_embedding.return_value = [0.1, 0.2, 0.3]
    mock_llm_agent.get_sparse_embedding.return_value = [1, 0, 1, 0]

    with patch.object(retriever, 'hybrid_search') as mock_hybrid_search, \
         patch.object(retriever, 'reranker') as mock_reranker, \
         patch.object(retriever, 'peloton_selection') as mock_peloton_selection:

        mock_hybrid_search.return_value = [Chunk("content", "container_uid", "doc_uid", "title", 1, "doc_title", "1", 1, 0.5)]
        mock_reranker.return_value = [Chunk("content", "container_uid", "doc_uid", "title", 1, "doc_title", "1", 1, 0.7)]
        mock_peloton_selection.return_value = [Chunk("content", "container_uid", "doc_uid", "title", 1, "doc_title", "1", 1, 0.7)]

        result = retriever.retrieve(query, condition)

        mock_llm_agent.get_embedding.assert_called_once_with(query)
        mock_llm_agent.get_sparse_embedding.assert_called_once_with(query)
        mock_hybrid_search.assert_called_once()
        mock_reranker.assert_called_once()
        mock_peloton_selection.assert_called_once()

        assert len(result) == 1
        assert isinstance(result[0], Chunk)

def test_retrieve_no_results(retriever, mock_llm_agent):
    query = "test query"
    condition = {"field": "value"}
    mock_llm_agent.get_embedding.return_value = [0.1, 0.2, 0.3]
    mock_llm_agent.get_sparse_embedding.return_value = [1, 0, 1, 0]

    with patch.object(retriever, 'hybrid_search') as mock_hybrid_search:
        mock_hybrid_search.return_value = []

        result = retriever.retrieve(query, condition)

        assert result == []

if __name__ == "__main__":
    pytest.main()