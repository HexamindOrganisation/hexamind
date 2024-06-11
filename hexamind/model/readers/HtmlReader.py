from bs4 import BeautifulSoup
import requests
from hexamind.model.readers.IReader import IReader
from hexamind.model.builder.MkBuilder import MkBuilder

class HtmlReader(IReader):

    def __init__(self, html_content: str):
        self.htlm_content = html_content
    
    
    def convert_to_htlm(self) -> str:
        return self.htlm_content
    
