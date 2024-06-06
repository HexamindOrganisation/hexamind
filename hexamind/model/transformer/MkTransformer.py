import markdown

from bs4 import BeautifulSoup

class MkTransformer:

    @classmethod
    def from_markdown(cls, markdown_content):
        htlm_content = markdown.markdown(markdown_content)
        soup = BeautifulSoup(htlm_content, features='html.parser')
        return cls.get_document_structure(soup)

    @staticmethod
    def table_to_string(table):
        table_content = '' 
        for row in table.find_all('tr'):
            row_text = ' | '.join(cell.get_text(strip=True) for cell in row.find_all(['td', 'th']))
            table_content += row_text + '\n'
        return table_content.strip()
    
    @classmethod
    def get_document_structure(cls, soup):
        """
        This method extracts the structure of the HTML document into a nested dictionary.

        Returns:
        - A nested dictionary representing the structure of the HTML document.
        """
        root_container = {'type' : 'container', 'children' : [], 'content' : None, 'level' : 0}
        hierarchy = [root_container]

        for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'table']):
            if element.name.startswith('h'):
                level = int(element.name[1])

                while len(hierarchy) > 1 and hierarchy[-1]['level'] >= level:
                    hierarchy.pop()
                
                leaf_container = {'type' : 'container', 'children' : [], 'content' : None, 'level' : level, 'parent' : hierarchy[-1]}
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
                table_content = cls.table_to_string(element)
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