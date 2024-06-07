from bs4 import BeautifulSoup
import requests
from hexamind.model.readers.IReader import IReader
from hexamind.model.builder.MkBuilder import MkBuilder

class HtmlReader(IReader):

    def __init__(self, html_content):
        self.soup = BeautifulSoup(html_content, 'html.parser')
    
    def _table_to_markdown(self, table):
        table_content = ''
        for row in table.find_all('tr'):
            row_text = ' | '.join(cell.get_text(strip=True) for cell in row.find_all(['td', 'th']))
            table_content += row_text + '\n'
        return table_content.strip()
    
    def _convert_to_markdown(self):
        markdown_content = ''
        for element in self.soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'table']):
            if element.name.startswith('h'):
                level = int(element.name[1])
                markdown_content += f"{'#' * level} {element.get_text(strip=True)}\n\n"
            elif element.name == 'p':
                text = element.get_text(strip=True)
                if text:
                    markdown_content += f"{text}\n\n"
            elif element.name == 'table':
                table_md = self._table_to_markdown(element)
                markdown_content += f"{table_md}\n\n"

        return markdown_content
    
