

from hexs_rag.model.readers.ExcelReader import ReaderExcel
import pytest

@pytest.mark.skip(reason="Test not implemented")
def test_reader_excel():
    # Test data file path
    example_file_path = "../hexs_rag/data/test_data/SampleData.xlsx"

    # Create an instance of ReaderExcel
    reader = ReaderExcel(example_file_path, sheet_name=1)

    # Assert that the reader instance has a 'paragraphs' attribute
    assert hasattr(reader, 'paragraphs'), "ReaderExcel object does not have a 'paragraphs' attribute"
    for paragraph in reader.paragraphs:
        assert paragraph.id_ is not None
        assert paragraph.page_id is not None
        assert paragraph.text is not None
    assert reader.paragraphs[0].text == "OrderDate: 2021-01-06 00:00:00 | Region: East | Rep: Jones | Item: Pencil | Units: 95 | Unit Cost: 1.99 | Total: 189.05"
    assert reader.paragraphs[0].page_id == 1
    assert reader.paragraphs[0].id_ == 211


                