from __future__ import (
    absolute_import, division, print_function, unicode_literals
)
import docx
import os
from docx.document import Document as _Document
from hexs_rag.model.model.Paragraph import Paragraph as ParagraphHexa
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph

class WordReader:
    """
    WordReader class that reads a word document and creates a list of paragraphs.
    """

    def __init__(self, path):
        self.path = path
        self.paragraphs = self.get_paragraphs()
    
