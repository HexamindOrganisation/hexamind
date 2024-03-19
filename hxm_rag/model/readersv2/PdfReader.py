import json
import os

# To extract text from tables in PDF
import pdfplumber as pdfp
import pypdf
import pytesseract
from pdf2image import convert_from_path
# To analyze the PDF layout and extract text
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTChar, LTFigure, LTTextContainer, LTTextBoxHorizontal
from PIL import Image
from collections import Counter

from hxm_rag.model.modelv2.container import Container
from hxm_rag.model.modelv2.block import Block
from hxm_rag.utils.utils.table_converter import table_converter


class PdfReader:
    def __init__(self, path, actual_first_page= 0, include_image=True):
        self.path = path
        self.root_container = dict()
        self.most_common_font_sizes = self.most_common_font_size()
        self.body_font_size = self.most_common_font_sizes[0][0]
        self.font_sizes = [font_size for font_size, count in self.most_common_font_sizes]
        self.actual_first_page = actual_first_page
        self.include_image = include_image


    def most_common_font_size(self):
        font_sizes = []

        for page_layout in extract_pages(self.path):
            for element in page_layout:
                if isinstance(element, LTTextBoxHorizontal):
                    for text_line in element:
                        for element in text_line:
                            if isinstance(element, LTChar):
                                font_sizes.append(round(element.size))
        
        font_size_count = Counter(font_sizes)
        most_common_font_sizes = font_size_count.most_common()
        return most_common_font_sizes
    
    def extract_table_to_text(self, page, table_settings=None):
        if table_settings is None:
            table_settings = dict()
        
        table = page.extract_table(table_settings)

        table_text = ''
        if table:
            for row in table:
                row_text = ' | '.join([str(cell) for cell in row])
                table_text += row_text + '\n'

        return table_text
    
    def pdf_manager(self):
        """
        Extracts text from a PDF and returns a dictionary with the structure of the document
        """
        pdfFileObj = open(self.path, "rb")
        pdfReaded = pypdf.PdfReader(pdfFileObj)
        number_of_pages = len(pdfReaded.pages)
        if self.actual_first_page > number_of_pages:
            page_numbers = None
        else:
            page_numbers = [i for i in range(self.actual_first_page - 1, number_of_pages)]

        last_font_size = None

        root_container = {
            'type' : 'container',
            'children' : [],
            'content' : '',
            'level' : 0
        }

        current_container = root_container

        with pdfp.open(self.path) as pdf:
            for page_number in page_numbers:
                page = pdf.pages[page_number]
                elements = page.extract_text(x_tolerance=3, y_tolerance=3)
                if elements:
                    for element in elements.split('\n'):
                        