import pytest
from hexs_rag.model.readers import PdfReader
from hexs_rag.model.model.paragraph import Paragraph
from unittest.mock import patch, MagicMock

MockElement = MagicMock()
MockElement.get_text.return_value = "hello world"
MockElement.styles = ['Bold', 'FontSize:12']

@pytest.fixture
def mock_pdf_path():
    return "data/test_data/pdf-test.pdf"

@pytest.fixture
def setup_pdfplumber_mock(mocker):
    mock_table = [['Column1', 'Column2'], ['Row1', 'Row2']]
    mock_page = MagicMock()
    mock_page.extract_tables.return_value = [mock_table]
    mock_pdf = MagicMock()
    mock_pdf.pages.__getitem__.return_value = mock_page

    mocker.patch('pdfplumber.open', MagicMock(return_value=mock_pdf))

@pytest.fixture
def setup_pytesseract_mock(mocker):
    mocker.patch('pytesseract.image_to_string', return_value="Extracted text from image")


def test_text_extraction(mock_pdf_path, setup_pdfplumber_mock):
    reader = PdfReader(path=mock_pdf_path)
    extracted_text, extracted_format = reader.text_extraction(MockElement)
    assert extracted_text == "hello world", "Text extraction failed"

def test_extract_table(mock_pdf_path, setup_pdfplumber_mock):
    reader = PdfReader(path=mock_pdf_path)
    table = reader.extract_table(pdf_path=mock_pdf_path, page_num=0, table_num=0)
    assert table == [['Column1', 'Column2'], ['Row1', 'Row2']], "Table extraction failed"

def test_pdf_manager_integration(mock_pdf_path, setup_pdfplumber_mock):
    reader = PdfReader(path=mock_pdf_path, actual_first_page_=1, include_images=True)
    paragraphs = reader.paragraphs

    assert len(paragraphs) > 0, "No paragraphs extracted"
    assert isinstance(paragraphs[0], Paragraph), "Paragraphs are not of type Paragraph"