import pytest
from hxm_rag.model.model.paragraph import Paragraph, INFINITE

def test_paragraph_initialization():
    paragraph = Paragraph("Example text", "title 1", 1, 1)
    assert paragraph.text == "Example text"
    assert paragraph.font_style == "title 1"
    assert paragraph.id_ == 211
    assert paragraph.page_id == 1
    assert paragraph.level == 1
    assert paragraph.is_structure

# Testing the blank property
@pytest.mark.parametrize("text, expected", [
    ("", True),
    ("\n", True),
    ("123", True),
    ("Example text", False),
    ("   ", True)
])
def test_paragraph_blank_property(text, expected):
    paragraph = Paragraph(text, "content", 1, 1)
    assert paragraph.blank is expected

# Testing the rearrange method
@pytest.mark.parametrize("font_style, expected_prefix", [
    ("code", "\n\nCode :```\n"),
    ("table", "\n\nTable :\n"),
    ("content", "")
])
def rearrange(font_style, expected_prefix):
    text = "Example text"
    paragraph = Paragraph(text, font_style, 1, 1)
    paragraph.rearrange()
    assert paragraph.text.startswith(expected_prefix)

# Testing handle_levels with different font styles
@pytest.mark.parametrize("font_style, expected_level", [
    ("title1", 1),
    ("heading 2", 2),
    ("subtitle 3", 3),
    ("titre 4", 4),
    ("sous-titre 5", 5),
    ("content", INFINITE),
    ("unrecognized", INFINITE),
    ("title", INFINITE),
    ("title abc", INFINITE)
])
def test_handle_levels(font_style, expected_level):
    paragraph = Paragraph("Example text", font_style, 1, 1)
    assert paragraph.level == expected_level

# TODO The logic is wierd for this one. May need an actual conversation
@pytest.mark.parametrize("font_style, expected_level", [
    ("title-1", 1),  # Incorrect delimiter
    ("heading two", INFINITE),  # Non-integer level
    (" ", INFINITE),  # Blank input
    ("title1extra", INFINITE),  # Additional characters without space
])
def test_handle_levels_with_malformed_input(font_style, expected_level):
    paragraph = Paragraph("Example text", font_style, 1, 1)
    assert paragraph.level == expected_level, f"handle_levels does not correctly handle malformed input '{font_style}'"

