#Description: doc class that initializes a document object, 
# processes it based on its file type, and structures its 
# content into a form that is more manageable and accessible 

from hexs_rag.model.model.paragraph import Paragraph
from hexs_rag.model.model.container import Container
from hexs_rag.utils.utils.index_creation import set_indexes
from hexs_rag.model.readers import ReaderExcel, HtmlReader, PdfReader, WordReader
import os
from typing import List

class Doc:
    """
    A class for abstracting the processing and handling of documents across various formats.
    
    This class supports reading documents in DOCX, PDF, HTML, and Excel/CSV formats,
    extracting their textual content into a structured format for further processing or analysis.
    
    Attributes:
        title (str): The title of the document, derived from the original file name.
        extension (str): The file extension, indicating the document format.
        id_ (int): A unique identifier for the instance of the document.
        path (str): The file path of the document.
        sheet_name (int): The name of the sheet within an Excel document to be processed.
        container (Container): A container holding the structured representation of the document's content.
        blocks (list): A list of blocks derived from the document's content, post-structuring.
    
    Parameters:
        path (str): The file path of the document. Defaults to an empty string.
        include_images (bool): Flag indicating whether to include images in the processing for PDFs. Defaults to True.
        actual_first_page (int): The actual starting page number for PDFs, useful for adjusting page numbers. Defaults to 1.
        sheet_name (int): The sheet name for Excel files to be processed. Defaults to 0.
    """

    def __init__(self, 
                path: str ='', 
                include_images: bool =True, 
                actual_first_page: int = 1,
                sheet_name: int = 0):

        file_name = os.path.basename(path) # get file and ext from path
        self.title, self.extension = os.path.splitext(file_name) # separate file and ext
        self.extension = self.extension.lower()
        self.actual_first_page = actual_first_page
        self.include_images = include_images 
        self.id_ = id(self)
        self.path = path  # Path of the temporary file for processing
        self.sheet_name = sheet_name
        self.paragraphs = self.read_document()
        self.container = Container(self.paragraphs, father=self, title=self.set_first_container_title(self.title, self.extension))
        set_indexes(self.container)
        self.blocks = self.get_blocks()

    def read_document(self) -> List[Paragraph]:
        """
        Reads the document using the appropriate reader based on the document's extension.
        Returns:
            list: A list of paragraphs extracted from the document.
        """
        if self.extension == '.docx':
            paragraphs = WordReader(self.path).paragraphs
        elif self.extension == '.pdf':
            paragraphs = PdfReader(self.path, self.actual_first_page, self.include_images).paragraphs
        elif self.extension == '.html':
            paragraphs = HtmlReader(self.path).paragraphs
        elif self.extension == '.xlsx' or self.extension == '.csv':
            paragraphs = ReaderExcel(self.path, sheet_name = self.sheet_name).paragraphs
        else:
            raise ValueError(f"Unsupported file format: {self.extension}. Supported formats are: \n .docx, .pdf, .html, .xlsx, .csv")
        return paragraphs
 

    @property
    def structure(self):
        """Returns the structured representation of the document's content."""
        return self.container.structure

    def get_blocks(self):
        """
        Processes the blocks within the document's container, assigning a document title and
        converting block indexes from lists to strings.
        
        Returns:
            list: The list of processed blocks with updated document titles and string indexes.
        """
        def from_list_to_str(index_list):
            index_str = str(index_list[0])
            for el in index_list[1:]:
                index_str += '.' + str(el)
            return index_str

        blocks = self.container.blocks
        for block in blocks:
            block.doc = self.title
            block.index = from_list_to_str(block.index)
        return blocks
    
    def set_first_container_title(self,
                                  title,
                                  extension) -> Paragraph:
        """
        Sets the initial container title based on the document's title and extension.
        
        Parameters:
            title (str): The title of the document.
            extension (str): The document's file extension.
        
        Returns:
            Paragraph: A Paragraph object representing the initial container title.
        """
        if extension == '.pdf':
            return Paragraph(text=title,font_style='title0',id_=0,page_id=0)
        elif extension == '.docx':
            return Paragraph(text=title,font_style='title0',id_=0,page_id=1)
        else:
            return Paragraph(text=title,font_style='h0',id_=0,page_id=1)
