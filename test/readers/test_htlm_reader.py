import pytest
from hexamind.model.readers.HtmlReader import HtmlReader

def test_htlm_to_markdown_conversion():
    htlm_content= "<h1>Title</h1><p>Some paragraph.</p><table><tr><td>Cell 1</td><td>Cell 2</td></tr></table>"
    reader = HtmlReader(htlm_content)
    expected_markdown = "# Title\n\nSome paragraph.\n\n| Cell 1 | Cell 2 |\n\n"
    assert reader.convert_to_markdown() == expected_markdown 

def test_empty_htlm():
    reader = HtmlReader('')
    assert reader.convert_to_markdown() == ''