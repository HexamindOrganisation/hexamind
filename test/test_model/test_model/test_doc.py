from hexs_rag.model.model.doc import Doc
import pytest


# fixtures allow us to define data that we can reuse for each test
# here we define an instance of the excel reader
@pytest.fixture 
def excel_instance():
    # Test data file paths
    example_file_path = "../hexs_rag/data/test_data/SampleData.xlsx"
    # Create an instance of Reader_HTML
    reader = Doc(path=example_file_path,
          include_images=True,
          actual_first_page=1)
    return reader

@pytest.fixture 
def html_instance():
    # Test data file paths
    example_file_path = "../hexs_rag/data/test_data/HTML5 Test Page.html"
    # Create an instance of Reader_HTML
    reader = Doc(path=example_file_path,
          include_images=True,
          actual_first_page=1)
    return reader

@pytest.fixture 
def word_instance():
    # Test data file paths
    example_file_path = "../hexs_rag/data/test_data/SampleDOCFile_500kb.doc"
    # Create an instance of Reader_HTML
    reader = Doc(path=example_file_path,
          include_images=True,
          actual_first_page=1)
    return reader

@pytest.fixture 
def pdf_instance():
    # Test data file paths
    example_file_path = "../hexs_rag/data/test_data/pdf-test.pdf"
    # Create an instance of Reader_HTML
    reader = Doc(path=example_file_path,
          include_images=True,
          actual_first_page=1)
    return reader


def test_excel_read(excel_instance):
    assert excel_instance is not None

def test_html_read(html_instance):
    assert html_instance is not None

def test_pdf_read(pdf_instance):
    assert pdf_instance is not None

def test_word_read(word_instance):
    assert word_instance is not None