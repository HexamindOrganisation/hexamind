import string

INFINITE = 10000

class Paragraph:
    """
    Paragraph class that represents the interface between the bloc and doc models and the container model. It handles the document hierarchy and structure.
    """
    def __init__(self, text : str, font_style : str, id_ : int, page_id : int):
        self.font_style = font_style
        self.id_ = int(str(2)+str(page_id)+str(id_))
        self.page_id = page_id
        self.level = self.handle_levels(font_style)
        self.is_structure = self.level < INFINITE
        self.text = text
    
    @property
    def blank(self):
        """
        checks if the paragraph is blank: i.e. it brings some signal (it may otherwise be ignored)
        """
        text = self.text.replace('\n', '')
        return set(text).isdisjoint(string.ascii_letters)   

    def rearrange_paragraph(self):
        """
        rearrange the paragraph to have a better structure
        """
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


            

