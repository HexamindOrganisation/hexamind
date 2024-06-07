from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os

import docx
from docx.document import Document
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import Table, _Cell
from docx.text.paragraph import Paragraph
from hexamind.model.readers.IReader import IReader
from collections import Counter
from hexamind.model.transformer.MkTransformer import MkTransformer

class WordReader(IReader):
    def __init__(self, path):
        self.path = path
        self.body_font_size = None
        self.body_bold_status = None
        self.headers = []

    def _iter_block_items(self, parent):
        if isinstance(parent, Document):
            parent_elm = parent.element.body
        elif isinstance(parent, _Cell):
            parent_elm = parent._tc
        else:
            raise ValueError("Unsupported parent type")

        for child in parent_elm.iterchildren():
            if isinstance(child, CT_P):
                yield Paragraph(child, parent)
            elif isinstance(child, CT_Tbl):
                yield Table(child, parent)
    
    def _detect_common_font_properties(self):
        doc = docx.Document(self.path)
        font_sizes = []
        bold_statuses = []

        for block in self._iter_block_items(doc):
            if isinstance(block, Paragraph):
                font_size = self._get_font_size(block)
                bold_status = self._is_bold(block)
                if font_size:
                    font_sizes.append(font_size)
                bold_statuses.append(bold_status)

        font_size_counter = Counter(font_sizes)

        if font_size_counter:
            most_common_font_sizes = font_size_counter.most_common()
            most_common_font_sizes.sort(key=lambda x: (-x[1], x[0]))
            self.body_font_size = most_common_font_sizes[0][0]
        
        bold_status_counter = Counter(bold_statuses)
        if bold_status_counter:
            self.body_bold_status = bold_status_counter.most_common(1)[0][0]
    
    def _get_font_size(self, paragraph):
        font_sizes = []
        for run in paragraph.runs:
            if run.font.size:
                font_sizes.append(run.font.size.pt)
            elif run.style.font.size:
                font_sizes.append(run.style.font.size.pt)
            elif paragraph.style.font.size:
                font_sizes.append(paragraph.style.font.size.pt)
            
        if font_sizes:
            return max(font_sizes)
        
        return None
    
    def _is_bold(self, paragraph):
        return any(run.bold for run in paragraph.runs)

    def _update_header_list(self, paragraph):
        current_font_size = self._get_font_size(paragraph)
        current_bold_status = self._is_bold(paragraph)
        level = 1

        if current_font_size is None:
            current_font_size = self.body_font_size
        print(f'Updating header list: {current_font_size}, {current_bold_status}')

        if self.headers:
            last_header = self.headers[-1]
            if current_font_size > last_header['font_size'] or (current_bold_status and not last_header['bold']):
                level = max(1, last_header['level'] - 1)
            elif current_font_size < last_header['font_size'] or (not current_bold_status and last_header['bold']):
                level = last_header['level'] + 1
            else:
                level = last_header['level']
        
        self.headers.append({
            'font_size': current_font_size,
            'bold': current_bold_status,
            'level': level
        })

        return level
    
    def _table_to_markdown(self, table):
        table_md = ''
        for row in table.rows:
            row_text = ' | '.join(cell.text.strip() for cell in row.cells)
            table_md += row_text + '\n'
        return table_md.strip()
        
    def convert_to_markdown(self):
        self._detect_common_font_properties()
        print(f"Body font : {self.body_font_size}")
        docx_document = docx.Document(self.path)
        markdown_content = ''

        for block in self._iter_block_items(docx_document):
            if isinstance(block, Paragraph):

                text = block.text.strip()
                
                if not text:
                    continue

                font_size = self._get_font_size(block)
                print(font_size)

                bold_status = self._is_bold(block)
                print(bold_status)

                if self._is_bold(block) or (self._get_font_size(block) and self._get_font_size(block) != self.body_font_size):
                    level = self._update_header_list(block)
                    print(level)
                    markdown_content += f"{'#' * (level)} {text}\n\n"
                else:
                    markdown_content += f"{text}\n\n"
            
            elif isinstance(block, Table):
                table_md = self._table_to_markdown(block)
                markdown_content += f"{table_md}\n\n"

        return markdown_content