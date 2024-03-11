import pytest
from hexs_rag.model.model.block import Block

def test_block_initialization():
    block = Block(doc='test_doc', title='test_title', content='test_content', index='test_index', rank=1, level=2, distance=3.0)

    assert block.doc == 'test_doc'
    assert block.title == 'test_title'
    assert block.content == 'test_content'
    assert block.index == 'test_index'
    assert block.rank == 1
    assert block.level == 2
    assert block.distance == 3.0

def test_block_distance_str():
    block = Block(distance=3.14159)
    assert block.distance_str == '3.14'


def test_from_dict():
    data = {
        'doc': 'test_doc',
        'title': 'test_title',
        'content': 'test_content',
        'index': 'test_index',
        'rank': 1,
        'level': 2,
        'distance': 3.0
    }
    block = Block.from_dict(data)

    assert block.doc == 'test_doc'
    assert block.title == 'test_title'
    assert block.content == 'test_content'
    assert block.index == 'test_index'
    assert block.rank == 1
    assert block.level == 2
    assert block.distance == 3.0

def test_to_dict():
    block = Block(doc='test_doc', title='test_title', content='test_content', index='test_index', rank=1, level=2, distance=3.0)
    expected_dict = {
        'doc': 'test_doc',
        'title': 'test_title',
        'content': 'test_content',
        'index': 'test_index',
        'rank': 1,
        'level': 2,
        'distance': 3.0
    }

    assert block.to_dict() == expected_dict

@pytest.mark.parametrize('data, expected_exception', [
    (['not','a','dict'], AssertionError),
    ({'not_a' :'valid_data'}, AssertionError),
    ({'doc': 1, 'title': 'test_title', 'content': 'test_content', 'index': 'test_index', 'rank': 1, 'level': 2, 'distance': 3.0}, AssertionError),])

def test_from_dict_with_invalid_data(data, expected_exception):
    with pytest.raises(expected_exception):
        Block.from_dict(data)