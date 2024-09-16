from hexamind.model.readers.IReader import IReader
from hexamind.model.builder.MkBuilder import MkBuilder
import markdown


class MarkdownReader(IReader):

    def __init__(self, markdown_content: str):
        self.markdown_content = markdown_content

    def convert_to_htlm(self) -> str:
        return markdown.markdown(self.markdown_content)
