# Description: HTML reader class designed to ingest HTML files

from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
import bs4
from hexs_rag.model.model.paragraph import Paragraph
from hexs_rag.utils.utils.table_converter import table_converter
from typing import List, Tuple
import os


class HtmlReader:
    """
    A class for reading and parsing HTML content to extract structured text data
    into a defined Paragraph format. The class processes HTML files, removing
    unnecessary tags (like script, style, and navigation elements) to focus on
    the main content. It supports formatting text content into paragraphs, lists,
    and tables, considering the semantics of HTML structure.

    Attributes:
        path (str): The file path of the HTML document to be read and parsed.
        paragraphs (List[Paragraph]): After initialization, this attribute holds
                                      a list of Paragraph objects that represent
                                      the structured text content extracted from
                                      the HTML file.

    Methods:
        read_html_with_beautifulsoup(): Parses the HTML file using BeautifulSoup,
                                        cleaning it of certain tags and extracting
                                        content into Paragraph objects based on
                                        textual elements and their styles.

        extract_paragraphs(elements): Processes HTML elements to extract and
                                      format them into Paragraph objects, considering
                                      the specific font styles and structuring as
                                      paragraphs.

        create_table(paragraphs, start_index): Parses table elements starting from
                                               a specific index in the paragraphs list,
                                               combining them into a single Paragraph
                                               object with formatted table content.

        create_list(paragraphs, start_index): Parses list elements (including nested lists)
                                              starting from a specific index in the paragraphs
                                              list, combining them into a single Paragraph
                                              object with formatted list content.

        format_list(list_content): Takes a nested list of strings and formats it into a
                                   single string that represents the list content in a
                                   structured text format.
    """

    def __init__(self, path: str):
        
        # handle errors
        if not isinstance(path, str):
            raise TypeError("Path must be a string")
        file_name = os.path.basename(path) # get file and ext from path
        self.title, self.extension = os.path.splitext(file_name) # separate file and ext
        self.extension = self.extension.lower()
        if self.extension != '.html':
            raise TypeError("file must be HTML")
        
        self.path = path
        self.paragraphs: List[Paragraph] = self.read_html_with_beautifulsoup()
        if not isinstance(self.paragraphs, list):
            raise TypeError(f"Error in Paragraphs in html reader are {type(self.paragraphs)}")
        
        for para in self.paragraphs:
            if not isinstance(para, Paragraph):
                raise TypeError("ERROR: HtmlReader paragraphs list contains non paragraph types")

    def read_html_with_beautifulsoup(self) -> List[Paragraph]:
        """Opens an HTML file and parses it into Paragraph objects, ignoring certain tags."""
        try:
            with open(self.path, "r", encoding='utf-8') as HTMLFile:
                content = HTMLFile.read()
                soup = BeautifulSoup(content, 'html.parser')
                self.remove_unwanted_tags(soup)
                leaf_elements = self.get_leaf_elements(soup)
                paragraphs = self.extract_paragraphs(leaf_elements)
                paragraphs = self.concatenate_paragraphs_with_same_font_style(paragraphs)
                # [p.rearrange() for p in paragraphs]
                return paragraphs
        except:
            raise Exception(f"Error in html read. \n file_path : {self.path}")

    def remove_unwanted_tags(self, soup: BeautifulSoup):
        """Removes script, style, and other non-content tags from the soup object."""
        for tag in soup(['style', 'script', 'footer', 'header', 'nav', 'aside', 'form']):
            tag.decompose()

    def get_leaf_elements(self, soup: BeautifulSoup) -> List[bs4.element.Tag]:
        """Gets all leaf elements in the HTML content."""
        return [elem for elem in soup.body.descendants if elem.name and not elem.find_all()]

    def extract_paragraphs(self, elements: List[bs4.element.Tag]) -> List[Paragraph]:
        """Creates a list of Paragraph objects from leaf elements."""
        return [Paragraph(text=elem.get_text(strip=True, separator='\n'), 
                          font_style=elem.name, id_=index, page_id=1)
                for index, elem in enumerate(elements) if elem.get_text(strip=True)]
     
    def concatenate_paragraphs_with_same_font_style(self, paragraphs: List[Paragraph]) -> List[Paragraph]:
        """Merges adjacent Paragraphs with the same font style into single Paragraphs."""
        concatenated_paragraphs = []
        for paragraph in paragraphs:
            if concatenated_paragraphs and paragraph.font_style == concatenated_paragraphs[-1].font_style:
                concatenated_paragraphs[-1].text += f"\n{paragraph.text}"
            else:
                concatenated_paragraphs.append(paragraph)
        return concatenated_paragraphs


    def create_table(self, paragraphs: List[Paragraph], i: int) -> List[Paragraph]:
        """
        Converts a sequence of Paragraph objects representing table headers and data cells
        into a single Paragraph object with a table representation.

        Parameters:
            paragraphs (List[Paragraph]): The list of Paragraph objects to process.
            i (int): The current index in the list to start processing from.

        Returns:
            List[Paragraph]: The updated list of Paragraph objects with the table inserted.
        """
        titles = self.extract_table_titles(paragraphs, i)
        content, i = self.extract_table_content(paragraphs, i, len(titles))
        table_paragraph = Paragraph(text=table_converter([titles] + content), 
                                    font_style="table", 
                                    id_=i, 
                                    page_id=1)
        # Insert the new table Paragraph object at the correct index
        paragraphs.insert(i, table_paragraph)
        return paragraphs

    def extract_table_titles(self, paragraphs: List[Paragraph], i: int) -> List[str]:
        """
        Extracts table titles from the Paragraph objects and removes those Paragraphs
        from the list.

        Parameters:
            paragraphs (List[Paragraph]): The list of Paragraph objects to process.
            i (int): The current index in the list to start processing from.

        Returns:
            List[str]: The list of table title strings.
        """
        titles = []
        while i < len(paragraphs) and paragraphs[i].font_style == "th":
            titles.append(paragraphs.pop(i).text)
        return titles

    def extract_table_content(self, paragraphs: List[Paragraph], i: int, num_titles: int) -> Tuple[List[List[str]], int]:
        """
        Extracts table content based on the number of titles and removes those Paragraphs
        from the list.

        Parameters:
            paragraphs (List[Paragraph]): The list of Paragraph objects to process.
            i (int): The current index in the list to start processing from.
            num_titles (int): The number of titles, which dictates the number of columns.

        Returns:
            Tuple[List[List[str]], int]: A tuple containing the list of table content and
                                         the next index to process.
        """
        content = []
        row = []
        for _ in range(num_titles):
            if i < len(paragraphs) and paragraphs[i].font_style == "td":
                row.append(paragraphs.pop(i).text)
            else:
                break  # Break if there are not enough td elements to form a row
        if len(row) == num_titles:  # Ensure the row has the correct number of columns
            content.append(row)
        return content, i
    
    def create_list(self, paragraphs, start_index: int) -> Tuple[List[Paragraph], int]:
        """
        Parses a list of Paragraph objects starting at a given index, handling nested lists
        and combining list item Paragraphs into a single Paragraph for each list.
        
        Parameters:
            paragraphs (List[Paragraph]): The list of Paragraph objects to be parsed.
            start_index (int): The index at which to start parsing list items.
        
        Returns:
            Tuple[List[Paragraph], int]: A tuple containing the updated list of Paragraphs
                                         and the next index to continue parsing from.
        """
        list_items = []  # Content of the list elements
        i = start_index  # Current index in the Paragraphs
        
        # Loop through paragraphs starting at index `i`, looking for list elements
        while i < len(paragraphs) and paragraphs[i].font_style in ["ul", "ol", "li"]:
            if paragraphs[i].font_style == "li":
                # Append the list item text and remove the paragraph as it's processed
                list_items.append(paragraphs[i].text)
                paragraphs.pop(i)
            elif paragraphs[i].font_style in ["ul", "ol"]:
                # If it's a nested list, recursively process the list
                sublist_items, new_index = self.create_list(paragraphs, i + 1)
                list_items.append(sublist_items)
                # Update index `i` as create_list can process multiple paragraphs
                i = new_index
            else:
                # Increment index `i` if the current paragraph isn't a list item
                i += 1
        
        # Convert the list content into the formatted string representation
        formatted_list = self.format_list(list_items)
        # Create a new Paragraph for the entire list
        list_paragraph = Paragraph(text=formatted_list, font_style="list", id_=start_index, page_id=1)
        # Insert the new Paragraph back into paragraphs at the original list start index
        paragraphs.insert(start_index, list_paragraph)

        return paragraphs, i

    def format_list(self, list_content):
        """
        Formats the contents of a list into a string representation.
        
        Parameters:
            list_content (List[str | List[str]]): The content of the list items, which can
                                                   be strings for simple list items or Lists
                                                   for nested items.
        
        Returns:
            str: A formatted string representation of the list.
        """
        formatted_result = ""
        for item in list_content:
            # Check if the item is a sublist
            if isinstance(item, list):
                # Recursively format the sublist
                formatted_result += f"{self.format_list(item)}\n"
            else:
                # Simply append the list item
                formatted_result += f"• {item}\n"

        return formatted_result.strip()  # Remove any trailing newline characters