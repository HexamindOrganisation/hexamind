import json
import PyPDF2
# To analyze the PDF layout and extract text
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LTFigure
# To extract text from tables in PDF
import pdfplumber as pdfp
from PIL import Image
from pdf2image import convert_from_path
import pytesseract 
import os
from hexs_rag.model.model.Paragraph import Paragraph
from hexs_rag.utils.utils.table_converter import table_converter
from hexs_rag.utils.model.pdfreader import *

