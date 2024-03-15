import re

INFINITE = 10000


def generate_paragraph_id(id: int, page_id: int) -> int:
    """Generates a unique paragraph ID."""
    return int(f"2{page_id}{id}")


def determine_level(font_style: str) -> int:
    """
    Determines the hierarchical level of the paragraph based on its font style.
    
    The font style typically indicates the paragraph's significance in the document's structure 
    (e.g., title, heading). This method translates the font style into a hierarchical level.
    """
    if font_style.startswith("title"):
        return extract_numeric_suffix(font_style, default=INFINITE)
    elif any(
        font_style.startswith(style)
        for style in ["heading", "subtitle", "titre", "sous-titre"]
    ):
        return extract_numeric_suffix(font_style)
    elif font_style == "content":
        return INFINITE
    else:
        return INFINITE


def extract_numeric_suffix(s: str, default: int = INFINITE) -> int:
    """ Extracts a numeric suffix from a string and returns it as an integer. """
    match = re.search(r"\d+$", s)
    return int(match.group()) if match else default


def rearrange_text(font_style, text):
    """
    Rearranges the paragraph text to enhance its structure based on the font style. 
    """
    # Handle unsupported font_style values gracefully
    if font_style not in ["code", "table"]:
        print(f"Unsupported font_style '{font_style}' for rearrangement.")
        return text
    if font_style == "code":
        text = "\n\nCode :```\n" + text + "\n```\n\n"
    elif font_style == "table":
        text = "\n\nTable :\n" + text + "\n\n"
    return text
