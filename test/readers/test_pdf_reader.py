import pytest
from hexamind.model.readers.PdfReader import PdfReader
import os
from unittest.mock import MagicMock


@pytest.fixture
def mock_logger():
    logger_mock = MagicMock()
    return logger_mock


@pytest.fixture
def pdf_reader():
    # Use the pre-existing dummy PDF file for testing purposes
    pdf_file_path = "./test/readers/dummy.pdf"
    return PdfReader(pdf_file_path)


def test_pdf_text_data(mock_logger, pdf_reader):
    # Check if the method runs and returns a list
    text_data = pdf_reader.pdf_text_data()
    assert isinstance(text_data, list)
    # Empty PDF should return an empty list
    assert len(text_data) == 586


def test_convert_to_htlm(mock_logger, pdf_reader, tmpdir):
    # Check if the HTML is written correctly
    content = pdf_reader.convert_to_htlm()

    # Expecting at least the basic HTML structure even if the PDF is empty
    assert "<html><body>" in content
    assert "</body></html>" in content


def test_font_list_def(mock_logger, pdf_reader):
    # Test the font_list_def method
    data = [("Sample text", 12), ("Another text", 14), ("Small text", 10)]
    sorted_sizes, most_common_size = pdf_reader.font_list_def(data)

    # Check if sorted_sizes is correctly sorted
    assert sorted_sizes == [14, 12, 10]
    # Most common size is one of the ones in the list
    assert most_common_size in sorted_sizes


def test_font_re_mapping(mock_logger, pdf_reader):
    # Test the font_re_mapping method
    data = [["Sample text", 12], ["Another text", 14], ["Small text", 10]]
    sizes = [14, 13, 10, 1]

    mapped_data = pdf_reader.font_re_mapping(data, sizes)

    # Check that the mapped data has the correct font sizes
    for item in mapped_data:
        assert item[1] in sizes


def test_aggregate_by_largest(mock_logger, pdf_reader):
    # Test the aggregate_by_largest method
    sorted_sizes = [18, 16, 14, 12, 10, 8]
    result = pdf_reader.aggregate_by_largest(sorted_sizes, 2)

    # Ensure the output is smaller or equal to the input
    assert len(result) <= len(sorted_sizes)
    # Ensure the first element is the largest one
    assert result[0] == 18