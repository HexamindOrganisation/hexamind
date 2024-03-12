import string

INFINITE = 10000

class Paragraph:
    """
    Paragraph class that represents the interface between the bloc and doc models and the container model. It handles the document hierarchy and structure.
    """
    def __init__(self, 
                text : str, 
                font_style : str, 
                id_ : int, 
                page_id : int):

        if not isinstance(text, str):
            raise ValueError("Text must be a string.")
        if not isinstance(font_style, str):
            raise ValueError("Font style must be a string.")
        if not isinstance(id_, int):
            raise ValueError("ID must be an integer.")
        if not isinstance(page_id, int):
            raise ValueError("Page ID must be an integer.")

        self.font_style = font_style

        try:
            self.id_ = int(str(2) + str(page_id) + str(id_))
        except ValueError as e:
            raise ValueError("Failed to compose ID from page_id and id_") from e


        self.page_id = page_id
        self.level = self.handle_levels(font_style)
        self.is_structure = self.level < INFINITE
        self.text = text
    
    @property
    def blank(self):
        """
        checks if the paragraph is blank: i.e. it brings some signal (it may otherwise be ignored)
        """
        if not self.text:  # Quick check for completely empty string
            return True
        text = self.text.replace('\n', '')
        return set(text).isdisjoint(string.ascii_letters)   

    def rearrange_paragraph(self):
        """
        rearrange the paragraph to have a better structure
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

    def handle_levels(self, font_style : str) -> int:
        """
        Handle the levels of the paragraph. 
        That means that it will assign to the paragraph a level that will be used to determine its position in the document hierarchy.
        """
        font_style = font_style.lower().strip()
        accepted_styles = ["heading", "title", "subtitle", "titre", "sous-titre"]

        if font_style.startswith("title"): # TODO implement more robust method (  re.findall(r'\d+', s) )
            try:
                level = int(font_style.replace('title', ''))
                return level if level > 0 else INFINITE
            except ValueError:
                return INFINITE

        elif any(font_style.startswith(style) for style in accepted_styles):
            try:
                level = int(font_style.split(' ')[-1]) # TODO implement more robust method (  re.findall(r'\d+', s) )
                return level
            except ValueError:
                return INFINITE
            
        elif font_style == "content":
            return INFINITE
        else:
            return INFINITE
    
    @property
    def structure(self):
        """
        returns the structure of the paragraph
        """
        return [self.level, self.id_]


            

