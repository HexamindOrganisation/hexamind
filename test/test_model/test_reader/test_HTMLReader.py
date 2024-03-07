
from hexs_rag.model.readers.HTMLreader import Reader_HTML
import pytest


# fixtures allow us to define data that we can reuse for each test
# here we define an instance of the html reader
@pytest.fixture 
def reader_instance():
    # Test data file paths
    example_file_path = "../hexs_rag/data/test_data/HTML5 Test Page.html"
    # Create an instance of Reader_HTML
    reader = Reader_HTML(example_file_path)
    return reader


def test_html_reader(reader_instance):
    """
    Check if the attributes are being set or not
    """
    # Assert that the reader instance has a 'paragraphs' attribute
    assert hasattr(reader_instance, 'paragraphs'), "Reader_HTML object does not have a 'paragraphs' attribute"
    for paragraph in reader_instance.paragraphs:
        assert paragraph.id_ is not None
        assert paragraph.page_id is not None
        assert paragraph.text is not None

def test_first_row(reader_instance):
    """
    Check if the first row has the correct values
    """
    assert reader_instance.paragraphs[0].text == "Heading 1"
    assert reader_instance.paragraphs[0].page_id == 1
    assert reader_instance.paragraphs[0].id_ == 210

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

def test_incorrect_file_format(): 
    """
    Check to break code
    """
    reader = Reader_HTML('../hexs_rag/data/test_data/business-financial-data-december-2023-quarter-csv.csv')
    # if an error occurs the reader simply sets the paragraphs attribute to an empty list
    assert reader.paragraphs == []

    
