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
        #self.root_container = dict()
        self.most_common_font_sizes = self.most_common_font_size()
        self.body_size = self.most_common_font_sizes[0][0]
        self.font_sizes = [font_size for font_size, count in self.most_common_font_sizes]
        self.max_font_size = self.get_max_font_size()
        self.actual_first_page = actual_first_page
        self.include_image = include_image
        self.font_size_hierarchy = self.get_font_size_hierarchy()

        self.root_container = self.add_to_structure()

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

    def get_max_font_size(self):
        #Get the max sized font of the document
        if self.font_sizes:
            max_font_size = max(self.font_sizes)
            return max_font_size
        else:
            return None
        
    def get_font_size_hierarchy(self):
        #get the font higher that the body size in a list based on the self.font_sizes list
        font_size_hierarchy = []
        for font_size in self.font_sizes:
            if font_size > self.body_size:
                font_size_hierarchy.append(font_size)
        return sorted(font_size_hierarchy, reverse=True)
    
    @staticmethod
    def analyze_line_font_size(line):
        # Analyzing the max occuring font size of the line
        font_sizes = []
        for element in line:
            if isinstance(element, LTChar):
                font_sizes.append(round(element.size))
        font_size_count = Counter(font_sizes)
        most_common_font_sizes = font_size_count.most_common()
        return most_common_font_sizes[0][0]
    
    def determine_level(self, font_size, last_font_size, max_font_size):
        # Determine hierarchical level of a line

        if font_size <= self.body_size:
                return 0, False
        
        is_header = font_size in self.font_size_hierarchy

        if is_header:
            new_level = self.font_size_hierarchy.index(font_size) + 1
        else:
            new_level = 0

        return new_level, is_header
    
    def add_to_structure(self):

        root_container = {'type' : 'container', 'children' : [], 'content' : None, 'level' : 0}

        current_container = root_container
        last_font_size = None
        body_size = self.body_size
        last_level = 0

        for page_layout in extract_pages(self.path):
            for element in page_layout:
                if isinstance(element, LTTextBoxHorizontal):
                    for line in element:
                        font_size = self.analyze_line_font_size(line)

                        level, is_header = self.determine_level(font_size, last_font_size, self.max_font_size)

                        if is_header:
                            while current_container['level'] >= level :
                                current_container = current_container.get('parent', root_container)
                            
                            header_container = {'type' : 'container', 'children' : [], 'content' : None, 'level' : level, 'parent' : current_container}
                            header_block_container = {'type' : 'container', 'children' : [], 'content' : None, 'level' : level + 1, 'parent' : header_container}
                            header_block = {'type' : 'block', 'content' : line.get_text(), 'level' : level + 1, 'parent' : header_block_container}

                            header_block_container['children'].append(header_block)
                            header_container['children'].append(header_block_container)
                            current_container['children'].append(header_container)
                            current_container = header_container
                        
                        else:
                            body_text = line.get_text()
                            new_block = {'type' : 'block', 'content' : body_text, 'level' : last_level+1, 'parent' : current_container}

                            if not current_container['children']:
                                block_container = {'type' : 'container', 'children' : [], 'content' : None, 'level' : last_level+1, 'parent' : current_container}
                                block_container['children'].append(new_block)
                                current_container['children'].append(block_container)
                            else:
                                current_container['children'][-1]['children'][0]['content'] += body_text
                    
                    last_level = level

        def remove_parent_ref(container):
            if 'parent' in container:
                del container['parent']
            for child in container.get('children', []):
                remove_parent_ref(child)
        
        remove_parent_ref(root_container)

        return root_container
