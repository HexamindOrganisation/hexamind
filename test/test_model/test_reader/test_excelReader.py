from hexs_rag.model.readers import ReaderExcel
from hexs_rag.model.model.paragraph import Paragraph
import pytest
import pandas as pd

def test_integration_with_real_file():
    reader = ReaderExcel(path="data/test_data/SampleData.xlsx")
    paragraphs = reader.paragraphs

    assert len(paragraphs)> 0, "No paragraphs found were created"
    assert isinstance(paragraphs[0], Paragraph), "The paragraphs created are not of the right type"

@pytest.fixture
def sample_excel_file():
    return pd.DataFrame({
        'col1': [1, 2, 3],
        'col2': [4, 5, 6],
        'col3': [7, 8, 9]
    })