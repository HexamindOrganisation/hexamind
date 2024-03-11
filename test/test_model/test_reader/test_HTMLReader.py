
from hexs_rag.model.readers.HTMLreader import HtmlReader
from hexs_rag.model.model.paragraph import Paragraph
from bs4 import BeautifulSoup
import pytest

# function and logic tests
def test_read_html_with_beautifulsoup(html_reader_instance):
    """Test that HTML content is correctly parsed into Paragraph objects."""
    assert html_reader_instance.paragraphs, "The paragraphs list should not be empty."

def test_remove_unwanted_tags(html_reader_instance):
    """Test that non-content tags are correctly removed from the soup object."""
    soup = BeautifulSoup(open(html_reader_instance.path, 'r', encoding='utf-8'), 'html.parser')
    initial_tag_count = len(soup.find_all(['script', 'style', 'footer', 'header', 'nav', 'aside', 'form']))
    html_reader_instance.remove_unwanted_tags(soup)
    final_tag_count = len(soup.find_all(['script', 'style', 'footer', 'header', 'nav', 'aside', 'form']))
    assert final_tag_count == 0, "All non-content tags should be removed."

def test_extract_paragraphs(html_reader_instance):
    """Test extraction of paragraphs from HTML elements."""
    soup = BeautifulSoup(open(html_reader_instance.path, 'r', encoding='utf-8'), 'html.parser')
    html_reader_instance.remove_unwanted_tags(soup)
    leaf_elements = html_reader_instance.get_leaf_elements(soup)
    paragraphs = html_reader_instance.extract_paragraphs(leaf_elements)
    assert paragraphs, "Paragraphs should be successfully extracted from leaf elements."

def test_concatenate_paragraphs_with_same_font_style(html_reader_instance):
    """Test concatenation of adjacent paragraphs with the same font style."""
    # Assuming a simplified implementation of Paragraph for demonstration
    paragraphs = [
        Paragraph(text="Paragraph 1", font_style="p", id_=0, page_id=1),
        Paragraph(text="Paragraph 2", font_style="p", id_=1, page_id=1),
        Paragraph(text="Heading", font_style="h1", id_=2, page_id=1),
        Paragraph(text="Paragraph 3", font_style="p", id_=3, page_id=1)
    ]
    concatenated = html_reader_instance.concatenate_paragraphs_with_same_font_style(paragraphs)
    assert len(concatenated) == 3, "Should concatenate adjacent paragraphs with the same font style."
    assert concatenated[0].text == "Paragraph 1\nParagraph 2", "Adjacent paragraphs with the same style should be merged."

def test_create_table(html_reader_instance):
    """Test parsing of table elements into a single Paragraph object."""
    # HTML includes a simple table structure to parse
    paragraphs = html_reader_instance.paragraphs 
    # Find the index where the table starts for simplicity
    start_index = next((i for i, p in enumerate(paragraphs) if p.font_style == "table"), None)
    if start_index is not None:
        updated_paragraphs = html_reader_instance.create_table(paragraphs, start_index)
        assert "table" in [p.font_style for p in updated_paragraphs], "A paragraph with font_style='table' should exist."

def test_create_list(html_reader_instance):
    """Test parsing of list elements into a single Paragraph object."""
    # HTML includes a list structure to parse
    paragraphs = html_reader_instance.paragraphs  #  paragraphs representing a list
    # Find the index where a list starts for simplicity
    start_index = next((i for i, p in enumerate(paragraphs) if p.font_style in ["ul", "ol"]), None)
    if start_index is not None:
        updated_paragraphs, _ = html_reader_instance.create_list(paragraphs, start_index)
        assert "list" in [p.font_style for p in updated_paragraphs], "A paragraph with font_style='list' should exist."

def test_format_list(html_reader_instance):
    """Test the formatting of a list into a structured text format."""
    list_content = ["Item 1", ["Item 2.1", "Item 2.2", ["Item 2.2.1"]], "Item 3"]
    formatted_list = html_reader_instance.format_list(list_content)
    assert formatted_list.count("•") == 5, "Should format list content with bullets for each item, including nested lists."

##############################################################################
# Error handling
def test_read_html_with_nonexistent_file():
    """Test reading from a file that does not exist."""
    with pytest.raises(Exception) as e_info:
        # HtmlReader must raise an exception for nonexistent files
        non_existent_path = 'nonexistent_file.html'
        reader = HtmlReader(non_existent_path)

def test_read_html_with_malformed_html(tmp_path):
    """Test parsing of a malformed HTML file."""
    # Create a temporary malformed HTML file
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "malformed.html"
    p.write_text("<html><head><title>Test</title></head><body><p>Paragraph without closing tag</body></html>")
    reader = HtmlReader(str(p))
    paragraphs = reader.read_html_with_beautifulsoup()
    assert paragraphs, "Should still parse paragraphs even from malformed HTML."

def test_create_table_with_no_table_structure(html_reader_instance):
    """Test handling of create_table method when no table structure is present."""
    # Assuming a simplified Paragraph structure and that create_table returns paragraphs unchanged if no table structure is found
    paragraphs = [Paragraph(text="Not a table", font_style="p", id_=0, page_id=1)]
    start_index = 0  # Starting from the first paragraph
    updated_paragraphs = html_reader_instance.create_table(paragraphs, start_index)
    assert len(updated_paragraphs) == len(paragraphs), "Should return paragraphs unchanged if no table structure is present."

def test_create_list_with_no_list_items(html_reader_instance):
    """Test create_list method when no list items are present."""
    paragraphs = [Paragraph(text="Not a list", font_style="p", id_=0, page_id=1)]
    start_index = 0
    updated_paragraphs, new_index = html_reader_instance.create_list(paragraphs, start_index)
    assert len(updated_paragraphs) == len(paragraphs), "Should return paragraphs unchanged if no list items are present."
    assert new_index == start_index, "New index should remain unchanged if no list items are found."

def test_read_html_with_incorrect_file_format(tmp_path):
    """Test attempting to read a file that is not HTML format."""
    # Create a temporary non-HTML (e.g., plain text) file
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "not_html.txt"
    p.write_text("This is not an HTML file.")
    with pytest.raises(Exception): # this should break
        reader = HtmlReader(str(p))

def test_html_reader_end_to_end(sample_html_file):
    """End-to-end test of HtmlReader from reading a file to extracting content."""
    reader = HtmlReader(sample_html_file)
    paragraphs = reader.paragraphs 
    # Assertions based on the expected output
    assert paragraphs, "Should extract content into paragraphs."
    assert any(p.text == "Document Heading" for p in paragraphs), "Should include the document heading."
    assert any(p.text == "This is a sample paragraph." for p in paragraphs), "Should include the sample paragraph."
    assert any(p.font_style == "h1" for p in paragraphs), "Should recognize an h1 heading."
    assert any(p.font_style == "td" for p in paragraphs), "Should recognize and parse tables."
