from hexs_rag.model.readers import ReaderExcel
from hexs_rag.model.model.paragraph import Paragraph
import pytest
import pandas as pd

@pytest.fixture
def mock_excel_path():
    return "data/test_data/SampleData.xlsx"

@pytest.fixture
def mock_csv_path():
    return "data/test_data/business-financial-data-december-2023-quarter-csv.csv"

def test_integration_with_real_file(mock_excel_path):
    reader = ReaderExcel(path=mock_excel_path)
    paragraphs = reader.paragraphs

    assert len(paragraphs)> 0, "No paragraphs found were created"
    assert isinstance(paragraphs[0], Paragraph), "The paragraphs created are not of the right type"

def test_integration_with_csv_file(mock_csv_path):
    reader = ReaderExcel(path=mock_csv_path)
    paragraphs = reader.paragraphs

    assert len(paragraphs)> 0, "No paragraphs found were created"
    assert isinstance(paragraphs[0], Paragraph), "The paragraphs created are not of the right type"

@pytest.mark.xfail(reason="This test is expected to fail")
def test_integration_with_excel_and_wrong_sheet_name(mock_excel_path):
    reader = ReaderExcel(path=mock_excel_path, sheet_name="wrong_sheet_name")
    paragraphs = reader.paragraphs

    assert len(paragraphs)> 0, "No paragraphs found were created"
    assert isinstance(paragraphs[0], Paragraph), "The paragraphs created are not of the right type"

def test_integration_with_excel_and_sheet_name(mock_excel_path):
    reader = ReaderExcel(path=mock_excel_path, sheet_name="Instructions")
    paragraphs = reader.paragraphs

    assert len(paragraphs)> 0, "No paragraphs found were created"
    assert isinstance(paragraphs[0], Paragraph), "The paragraphs created are not of the right type"


def test_paragraph_content(mock_excel_path):
    reader = ReaderExcel(path=mock_excel_path, sheet_name="SalesOrders")
    paragraphs = reader.paragraphs

    expected_first_paragraph = "OrderDate: 2021-01-06 00:00:00 | Region: East | Rep: Jones | Item: Pencil | Units: 95 | Unit Cost: 1.99 | Total: 189.05"

    assert paragraphs[0].text == expected_first_paragraph, "The paragraph content is not as expected"

def test_unsupported_file_extension():
    with pytest.raises(ValueError) as e:
        reader = ReaderExcel(path="data/test_data/HTML5 Test Page.html")
    
    assert "Unsupported file extension: " in str(e.value), "The reader did not raise an exception for an unsupported file extension"

def test_get_sheet_number(mock_excel_path):
    reader = ReaderExcel(path=mock_excel_path)
    sheet_number = reader.get_sheet_number()

    assert sheet_number == 3, "The sheet number is not as expected"