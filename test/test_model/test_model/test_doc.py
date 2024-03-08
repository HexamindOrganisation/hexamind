from hexs_rag.model.model.doc import Doc
import pytest


# fixtures allow us to define data that we can reuse for each test
# here we define an instance of the html reader
@pytest.fixture 
def reader_instance():
    # Test data file paths
    example_file_path = "../hexs_rag/data/test_data/SampleData.xlsx"
    # Create an instance of Reader_HTML
    reader = doc = Doc(path=example_file_path,
          include_images=True,
          actual_first_page=1)
    return reader

def test_exists(reader_instance):
    assert reader_instance is not None