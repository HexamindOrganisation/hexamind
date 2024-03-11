#Description: define fixtures used within other tests

import pytest
from hexs_rag.model.model.doc import Doc

@pytest.fixture 
def doc_excel_instance():
    # Test data file paths
    excel_file_path = "../hexs_rag/data/test_data/SampleData.xlsx"
    # Create an instance of Reader_HTML
    return Doc(path=excel_file_path,
          include_images=True,
          actual_first_page=1)


@pytest.fixture 
def doc_html_instance():
    # Test data file paths
    html_file_path = "../hexs_rag/data/test_data/HTML5 Test Page.html"
    # Create an instance of Reader_HTML
    return Doc(path=html_file_path,
          include_images=True,
          actual_first_page=1)
   

@pytest.fixture 
def doc_word_instance():
    # Test data file paths
    docx_file_path = "../hexs_rag/data/test_data/sample_doc.docx"
    # Create an instance of Reader_HTML
    return Doc(path=docx_file_path,
          include_images=True,
          actual_first_page=1)


@pytest.fixture 
def doc_pdf_instance():
    # Test data file paths
    pdf_file_path = "../hexs_rag/data/test_data/pdf-test.pdf"
    # Create an instance of Reader_HTML
    return Doc(path=pdf_file_path,
          include_images=True,
          actual_first_page=1)