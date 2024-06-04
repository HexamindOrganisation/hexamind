from bs4 import BeautifulSoup
import requests

class HtmlReader:
    def __init__(self, html_content):
        self.soup = BeautifulSoup(html_content, 'html.parser')
        self.document_structure = self.get_document_structure()
    
    def iter_block_items(self, parent):
        for child in parent.children:
            if child.name in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'table']:
                yield child
            
    def table_to_string(self, table):
        table_content = '' 
        for row in table.find_all('tr'):
            row_text = ' | '.join(cell.get_text(strip=True) for cell in row.find_all(['td', 'th']))
            table_content += row_text + '\n'
        return table_content.strip()
    
    def get_document_structure(self):
        root_container = {'type' : 'container', 'children' : [], 'content' : None, 'level' : 0}
        hierarchy = [root_container]

        for element in self.soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'table']):
            if element.name.startswith('h'):
                level = int(element.name[1])

                while len(hierarchy) > 1 and hierarchy[-1]['level'] >= level:
                    hierarchy.pop()
                
                leaf_container = {'type' : 'container', 'children' : [], 'content' : None, 'level' : level+1, 'parent' : hierarchy[-1]}
                header_block = {'type' : 'block', 'content' : element.get_text(strip=True), 'level' : leaf_container['level'], 'parent' : hierarchy[-1]}
                new_container = {'type' : 'container', 'children' : [], 'content' : None, 'level' : level, 'parent' : hierarchy[-1]}
                leaf_container['children'].append(header_block)
                new_container['children'].append(leaf_container)
                hierarchy[-1]['children'].append(new_container)
                hierarchy.append(new_container)
            
            elif element.name == 'p':
                text = element.get_text(strip=True)
                if text:
                    leaf_container = {'type' : 'container', 'children' : [], 'content' : None, 'level' : hierarchy[-1]['level'], 'parent' : hierarchy[-1]}
                    new_block = {'type' : 'block', 'content' : text, 'level' : leaf_container['level'], 'parent' : hierarchy[-1]}
                    leaf_container['children'].append(new_block)
                    hierarchy[-1]['children'].append(leaf_container)
             
            elif element.name == 'table':
                table_content = self.table_to_string(element)
                leaf_container = {'type' : 'container', 'children' : [], 'content' : None, 'level' : hierarchy[-1]['level'], 'parent' : hierarchy[-1]}
                new_block = {'type' : 'block', 'content' : table_content, 'level' : leaf_container['level'] , 'parent' : hierarchy[-1]}
                leaf_container['children'].append(new_block)
                hierarchy[-1]['children'].append(leaf_container)
        
        def remove_parent_ref(container):
            container.pop('parent', None)
            for child in container.get('children', []):
              if child['type'] == 'container':
                  remove_parent_ref(child)

        remove_parent_ref(root_container)
        
        return root_container