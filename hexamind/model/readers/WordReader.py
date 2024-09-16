from __future__ import absolute_import, division, print_function, unicode_literals

import os

import docx
from docx.document import Document
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import Table, _Cell
from docx.text.paragraph import Paragraph
from hexamind.model.readers.IReader import IReader
from collections import Counter
import mammoth


class WordReader(IReader):
    def __init__(self, path: str):
        self.path = path

    def convert_to_htlm(self) -> str:
        with open(self.path, "rb") as docx_file:
            result = mammoth.convert_to_html(docx_file)
            return result.value
