from bs4 import BeautifulSoup
import requests
from hexamind.model.readers.IReader import IReader
from hexamind.model.builder.MkBuilder import MkBuilder


class HtmlReader(IReader):

    def __init__(self, html_path: str):
        self.html_path = html_path

    def convert_to_htlm(self) -> str:
        with open(self.html_path, "r", encoding="utf-8") as file:
            html_content = file.read()
        return html_content
