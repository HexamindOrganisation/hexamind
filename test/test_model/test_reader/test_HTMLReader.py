
from hexs_rag.model.readers.HTMLreader import Reader_HTML
import pytest


def test_html_reader():
    """
    Check if the attributes are being set or not
    """
    # Test data file paths
    example_file_path = "../hexs_rag/data/test_data/HTML5 Test Page.html"
    # Create an instance of Reader_HTML
    reader = Reader_HTML(example_file_path)
    # Assert that the reader instance has a 'paragraphs' attribute
    assert hasattr(reader, 'paragraphs'), "Reader_HTML object does not have a 'paragraphs' attribute"
    for paragraph in reader.paragraphs:
        assert paragraph.id_ is not None
        assert paragraph.page_id is not None
        assert paragraph.text is not None

def test_first_row():
    """
    Check if the first row has the correct values
    """
    # Test data file paths
    example_file_path = "../hexs_rag/data/test_data/HTML5 Test Page.html"
    # Create an instance of Reader_HTML
    reader = Reader_HTML(example_file_path)
    assert reader.paragraphs[0].text == "Heading 1"
    assert reader.paragraphs[0].page_id == 1
    assert reader.paragraphs[0].id_ == 210

def test_table_format(): # TODO
    """
    Check if tables are being correctly formatted
    """
    pass

def test_list_format(): # TODO
    """
    Check if lists are correctly formatted
    """
    pass

def test_error_handling(): # TODO
    """
    Check to break code
    """
    pass
    
