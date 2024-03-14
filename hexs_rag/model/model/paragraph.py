import re
import string

INFINITE = 10000

class Paragraph:
    """
    Paragraph class represents a segment of text within a document, holding information about its content, 
    style, and its position within the document's hierarchy.
    
    Attributes:
        text (str): The text content of the paragraph.
        font_style (str): The font style of the paragraph, indicating its structural significance (e.g., title, heading).
        id_ (int): A unique identifier for the paragraph.
        page_id (int): The page number on which the paragraph is located.
        level (int): The level in the document hierarchy determined by the font_style.
        is_structure (bool): A flag indicating whether the paragraph is a structural element (like a title or heading).
    """

    def __init__(self, 
                text: str, 
                font_style: str, 
                id_: int, 
                page_id: int):
                
        self.text = text.strip()
        self.font_style = font_style.strip().lower()
        self.id_ = self._generate_id(id_, page_id)
        self.page_id = page_id
        self.level = self._determine_level(font_style)
        self.is_structure = self.level < INFINITE
        self = self.rearrange()

    def _generate_id(self, id_: int, page_id: int) -> int:
        """ Generates a unique ID for the paragraph using the page ID and paragraph ID. """
        try:
            return int(f"2{page_id}{id_}")
        except ValueError as e:
            raise ValueError(f"Failed to compose ID from page_id and id_: {e}")

    def _determine_level(self, 
                        font_style: str) -> int:
        """
        Determines the hierarchical level of the paragraph based on its font style.
        
        The font style typically indicates the paragraph's significance in the document's structure 
        (e.g., title, heading). This method translates the font style into a hierarchical level.
        """
        if font_style.startswith("title"):
            return self._extract_numeric_suffix(font_style, default=INFINITE)
        elif any(font_style.startswith(style) for style in ["heading", "subtitle", "titre", "sous-titre"]):
            return self._extract_numeric_suffix(font_style)
        elif font_style == "content":
            return INFINITE
        else:
            return INFINITE

    def _extract_numeric_suffix(self, 
                                s: str, 
                                default: int = INFINITE) -> int:
        """ Extracts a numeric suffix from a string and returns it as an integer. """
        match = re.search(r'\d+$', s)
        return int(match.group()) if match else default

    @property
    def blank(self) -> bool:
        """ Returns True if the paragraph contains only whitespace or non-letter characters; False otherwise. """
        return not self.text.strip() or set(self.text).isdisjoint(string.ascii_letters)

    def rearrange(self):
        """
        Rearranges the paragraph text to enhance its structure based on the font style. 
        """
        # Handle unsupported font_style values gracefully
        if self.font_style not in ["code", "table"]:
            print(f"Unsupported font_style '{self.font_style}' for rearrangement.")
            return self
        
        if self.font_style == "code":
            self.text = "\n\nCode :```\n" + self.text + "\n```\n\n"
        elif self.font_style == "table":
            self.text = "\n\nTable :\n" + self.text + "\n\n"
        return self


# from hexs_rag.utils.model.paragraph import generate_paragraph_id, determine_level, rearrange_text

# class Paragraph:
#     """
#     Represents a segment of text within a document, holding information about its content, 
#     style, and position within the document's hierarchy.
#     """

#     def __init__(self, text: str, font_style: str, id: int, page_id: int):
#         self.text = text.strip()
#         self.font_style = font_style.strip().lower()
#         self.id = generate_paragraph_id(id, page_id)
#         self.page_id = page_id
#         self.level = determine_level(self.font_style)
#         self.is_structure = self.level < INFINITE
#         self.rearrange()

#     @property
#     def blank(self) -> bool:
#         """Checks if the paragraph is blank."""
#         return not self.text or set(self.text).isdisjoint(string.ascii_letters)

#     def rearrange(self):
#         """Enhances paragraph structure based on font style."""
#         self.text = rearrange_text(self.text, self.font_style)
