import json
import os

# To extract text from tables in PDF
import pdfplumber as pdfp
import pypdf
import pytesseract
from pdf2image import convert_from_path
# To analyze the PDF layout and extract text
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTChar, LTFigure, LTTextContainer
from PIL import Image

from hxm_rag.model.modelv2.container import Container
from hxm_rag.model.modelv2.block import Block
from hxm_rag.utils.utils.table_converter import table_converter


class PdfReader:
    def __init__(self, path, actual_first_page= 0, include_image=True):
        self.path = path
        self.root_container = self.pdf_manager(actual_first_page, include_image)
    
    def most_occuring_fonts(self, line_formats: list):
            """_summary_

            Args:
                line_formats (list): _description_

            Returns:
                _type_: _description_
            """
            if line_formats != []:
                min_freq = 3
                font_size_freq = {
                    i: line_formats.count(i)
                    for i in set(line_formats)
                    if isinstance(i, float)
                }
                most_occuring_font_sizes = [
                    size for size, freq in font_size_freq.items() if freq >= min_freq
                ]
                line_formats = [
                    i
                    for i in line_formats
                    if i in most_occuring_font_sizes or isinstance(i, str)
                ]
            return line_formats

    """ def text_extraction(self, element):
        # Extracting the text from the in line text element
        line_text = element.get_text()
        # Find the formats of the text
        # Initialize the list with all the formats appeared in the line of text
        line_formats = []
        for text_line in element:
            if isinstance(text_line, LTTextContainer):
                # Iterating through each character in the line of text
                for character in text_line:
                    if isinstance(character, LTChar):
                        # Append the font name of the character
                        line_formats.append(character.fontname)
                        # Append the font size of the character
                        line_formats.append(character.size)
        # find the most occuring font size and keep it. If there are more than one, keep all of them.
        line_formats = self.most_occuring_fonts(line_formats)
        # Find the unique font sizes and names in the line and delete the None values
        format_per_line = list(set(line_formats))
        # Return a tuple with the text in each line along with its format
        return (line_text, format_per_line) """

    def extract_table(self, pdf_path, page_num, table_num):
        """_summary_

        Args:
            pdf_path (_type_): _description_
            page_num (_type_): _description_
            table_num (_type_): _description_

        Returns:
            _type_: _description_
        """
        # Open the pdf file
        pdf = pdfp.open(pdf_path)
        # Find the examined page
        table_page = pdf.pages[page_num]
        # Extract the appropriate table
        table = table_page.extract_tables()[table_num]

        return table

    def is_element_inside_any_table(self, element, page, tables):
        """_summary_

        Args:
            element (_type_): _description_
            page (_type_): _description_
            tables (_type_): _description_

        Returns:
            _type_: _description_
        """
        x0, y0up, x1, y1up = element.bbox
        # Change the cordinates because the pdfminer counts from the botton to top of the page
        y0 = page.bbox[3] - y1up
        y1 = page.bbox[3] - y0up
        for table in tables:
            tx0, ty0, tx1, ty1 = table.bbox
            if tx0 <= x0 <= x1 <= tx1 and ty0 <= y0 <= y1 <= ty1:
                return True
        return False

# Function to find the table for a given element
    def find_table_for_element(self, element, page, tables):
        """_summary_

        Args:
            element (_type_): _description_
            page (_type_): _description_
            tables (_type_): _description_

        Returns:
            _type_: _description_
        """
        x0, y0up, x1, y1up = element.bbox
        # Change the cordinates because the pdfminer counts from the botton to top of the page
        y0 = page.bbox[3] - y1up
        y1 = page.bbox[3] - y0up
        for i, table in enumerate(tables):
            tx0, ty0, tx1, ty1 = table.bbox
            if tx0 <= x0 <= x1 <= tx1 and ty0 <= y0 <= y1 <= ty1:
                return i  # Return the index of the table
        return None

# Create a function to crop the image elements from PDFs
    def crop_image(self, element, pageObj):
        """_summary_

        Args:
            element (_type_): _description_
            pageObj (_type_): _description_
        """
        # Get the coordinates to crop the image from PDF
        [image_left, image_top, image_right, image_bottom] = [
            element.x0,
            element.y0,
            element.x1,
            element.y1,
        ]
        # Crop the page using coordinates (left, bottom, right, top)
        pageObj.mediabox.lower_left = (image_left, image_bottom)
        pageObj.mediabox.upper_right = (image_right, image_top)
        # Save the cropped page to a new PDF
        cropped_pdf_writer = pypdf.PdfWriter()
        cropped_pdf_writer.add_page(pageObj)
        # Save the cropped PDF to a new file
        with open("cropped_image.pdf", "wb") as cropped_pdf_file:
            cropped_pdf_writer.write(cropped_pdf_file)

# Create a function to convert the PDF to images
    def convert_to_images(
        self, input_file,
    ):
        """_summary_

        Args:
            input_file (_type_): _description_
        """
        images = convert_from_path(input_file)
        image = images[0]
        output_file = "PDF_image.png"
        image.save(output_file, "PNG")

# Create a function to read text from images
    def image_to_text(self, image_path):
        """_summary_

        Args:
            image_path (_type_): _description_

        Returns:
            _type_: _description_
        """
        # Read the image
        img = Image.open(image_path)
        # Extract the text from the image
        text = pytesseract.image_to_string(img)
        return text

    def is_potential_header(self, element):

        HEADER_FONT_SIZE_THRESHOLD = 13

        font_size = self.get_font_size_of_text_element(element)

        return font_size >= HEADER_FONT_SIZE_THRESHOLD

    @staticmethod
    def get_font_size_of_text_element(element):
        
        font_sizes = []

        for text_line in element:
            if isinstance(text_line, LTTextContainer):
                for character in text_line:
                    if isinstance(character, LTChar):
                        font_sizes.append(character.size)
        if font_sizes:
            return max(font_sizes)

    @staticmethod
    def text_extraction(element):
        return element.strip()

    def pdf_manager(self, actual_first_page=0, include_images=True):

        root_container = Container(None, None, 0)
        current_container = root_container
        last_header_font_size = None # Used to track the last header font size to determine if the next container will be at the same level or not

        with pdfp.open(self.path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                for element in page.extract_text():
                    if isinstance(element, LTTextContainer):
                        if self.is_potential_header(element):
                            header_font_size = self.get_font_size_of_text_element(element)
                            if last_header_font_size is not None and header_font_size < last_header_font_size:
                                current_container = current_container.parent_container
                                last_header_font_size = header_font_size
                                sub_container = Container(root_container.parent_document, current_container, current_container.level + 1)
                                current_container.add_child(sub_container)
                                current_container = sub_container
                            elif last_header_font_size is None or header_font_size == last_header_font_size:
                                sibling_container = Container(root_container.parent_document, current_container.parent_container, current_container.level)
                                current_container.parent_container.add_child(sibling_container)
                                current_container = sibling_container
                            elif header_font_size > last_header_font_size:
                                sub_container = Container(root_container.parent_document, current_container, current_container.level + 1)
                                current_container.add_child(sub_container)
                                current_container = sub_container
                                last_header_font_size = header_font_size
                            else:
                                text = self.text_extraction(element)
                                block = Block(text, root_container.parent_document, current_container)
                                current_container.add_child(block)
        
        return root_container

