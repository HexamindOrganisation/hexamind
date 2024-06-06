from bs4 import BeautifulSoup
import requests
from hexamind.model.readers.IReader import IReader

class HtmlReader(IReader):
    """
    This class reads a HTLM document and extracts its structure into a nested dictionary.

    The structure of the dictionary is as follows:
    {
        'type' : 'container' or 'block',
        'children' : [list of nested dictionaries],
        'content' : None or string,
        'level' : int,
        'parent' : parent dictionary
    }

    The 'type' key indicates if the dictionary represents a container or a block.

    The 'children' key contains a list of nested dictionaries that represent the children of the current dictionary.

    The 'content' key contains the text content of the block or container. If the dictionary represents a container, the content is None.

    The 'level' key contains the level of the block or container in the hierarchy.

    The 'parent' key contains a reference to the parent dictionary in the hierarchy.

    """
    def __init__(self, html_content):
        self.soup = BeautifulSoup(html_content, 'html.parser')
    
    def table_to_markdown(self, table):
        table_content = ''
        for row in table.find_all('tr'):
            row_text = ' | '.join(cell.get_text(strip=True) for cell in row.find_all(['td', 'th']))
            table_content += row_text + '\n'
        return table_content.strip()
    
    def convert_to_markdown(self):
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
                table_md = self.table_to_markdown(element)
                markdown_content += f"{table_md}\n\n"

        return markdown_content