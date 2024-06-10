from hexamind.model.readers.IReader import IReader
from hexamind.model.builder.MkBuilder import MkBuilder

class MarkdownReader(IReader):

    def __init__(self, markdown_content : str):
        self.markdown_content = markdown_content

    def convert_to_markdown(self):
        return self.markdown_content
    