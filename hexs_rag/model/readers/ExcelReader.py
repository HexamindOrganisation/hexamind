# Description: Excel file reader

import os
import pandas as pd
from hexs_rag.model.model.paragraph import Paragraph

# TODO handle case where there are multiple sheets for ingestion

class ReaderExcel: 
    """
    -----------------------
    Reader method that ingests Excel files and converts into a list of 
    paragraphs in the following format: 
    Colname1: Col1Row1Val | colName2: Col2Row1Val| colName3: Col3Row1Val
    ------------------------
    Attributes:
    path: str 
        Path towards excel file
    sheet_name: str, int, list, or None, default 0
        Strings are used for sheet names. 
        Integers are used in zero-indexed sheet positions 
        (chart sheets do not count as a sheet position). 
        Lists of strings/integers are used to request multiple sheets.
    paragraphs: list
        List of paragraphs created from the excel file
    sheet_number: int
        Number of sheets in the Excel file
    filename: str
        Name of the file
    file_extension: str
        File extension of the file

    Methods:
    read_dataframe()
        Read data from an Excel or CSV file into a DataFrame.
    get_paragraphs()
        Extracts paragraphs of text from a DataFrame which is read from an Excel or CSV file.
    get_sheet_number()
        Returns the number of sheets in the Excel file.

    Raises:
    ValueError: Unsupported file extension
    """
    def __init__(self, 
                path: str, 
                sheet_name = 0):
        self.path = path
        self.sheet_name = sheet_name
        self.sheet_number = None
        self.filename, self.file_extension = os.path.splitext(self.path)
        if self.file_extension not in ['.xlsx', '.csv']:
            raise ValueError(f"Unsupported file extension: {self.file_extension}")
        if self.file_extension == ".xlsx":
            self.sheet_number = self.get_sheet_number()

        self.paragraphs = self.get_paragraphs()

  
    def read_dataframe(self):
        # TODO add more formats + further parameters for df ingestion. 
        """Read data from an Excel or CSV file into a DataFrame.

        Determines the file type based on the file extension and reads
        the data into a pandas DataFrame. Currently supports '.xlsx' and
        '.csv' file extensions.

        Returns:
            DataFrame: The data from the file as a pandas DataFrame.
        """
        # Check the file extension and read the file into a DataFrame accordingly
        if self.file_extension == '.xlsx':
            if self.sheet_name is None:
                # For Excel files, use the pd.read_excel function
                df = pd.read_excel(self.path, sheet_name=0)
            else:
                try:
                    df = pd.read_excel(self.path, sheet_name=self.sheet_name)
                except:
                    raise ValueError(f"Sheet name {self.sheet_name} not found in the file")
        elif self.file_extension == '.csv':
            # For CSV files, use the pd.read_csv function
            df = pd.read_csv(self.path)
        return df

    def get_paragraphs(self, 
                    max_paragraph_length: int = 1000, 
                    rows_per_page: int = 50):
        """
        Extracts paragraphs of text from a DataFrame which is read from an Excel or CSV file.
        
        This method organizes content into paragraphs, with each paragraph consisting of text 
        from one or more rows of the DataFrame, concatenated and separated by vertical bars. 
        Each paragraph has a maximum length, and the text is split across multiple paragraphs 
        if this length is exceeded. Additionally, paragraphs are associated with page numbers, 
        simulating pagination based on a specified number of rows per page.
        
        Parameters:
        max_paragraph_length (int): The maximum character length a paragraph can have before 
                                    it is split into a new paragraph.
        rows_per_page (int): The number of DataFrame rows to consider for each 'page' when 
                            assigning page IDs to paragraphs.
        
        Returns:
        list: A list of Paragraph objects, each containing the text from the DataFrame, 
            the paragraph's style (hardcoded as 'Normal' for all paragraphs), the unique 
            paragraph ID, and the page ID.
        
        The first row of the DataFrame is treated separately and is always turned into the 
        first paragraph with ID 1. Subsequent paragraphs start with ID 2 and are constructed 
        from the remaining rows. Page IDs start at 1 and are incremented after every 
        `rows_per_page` row is processed.
        """
        df = self.read_dataframe()

        paragraphs = [] # empty list to recieve paragraph info
        
        # gets top row information in the format: 
        # Colname1: Col1Row1Val | colName2: Col2Row1Val| colName3: Col3Row1Val 
        first_row_text = ' | '.join([f"{col}: {df.iloc[0][col]}" \
                        for col in df.columns \
                        if pd.notnull(df.iloc[0][col])])
        paragraphs.append(Paragraph(first_row_text, 'Normal', 1, 1))  # Append the first row as a separate paragraph
        
        # initialise variables
        paragraph_lines = []
        current_page_id = 1
        paragraph_id = 2  # Start with 2 since the first row has already been added

        for index, row in df.iloc[1:].iterrows():  # iterate through the rest of the rows
            # Concatenate text from multiple columns with column names
            row_text = ' | '.join([f"{col}: {row[col]}" for col in df.columns if pd.notnull(row[col])])

            # Accumulate paragraph lines
            paragraph_lines.append(row_text)

            # Check if the maximum paragraph length is reached or if it's the last row
            if sum(len(line) for line in paragraph_lines) >= max_paragraph_length or index == len(df) - 1:
                # Join lines to form a paragraph
                current_paragraph = ' '.join(paragraph_lines)

                # Create and append the Paragraph object
                paragraphs.append(Paragraph(current_paragraph, 'Normal', paragraph_id, current_page_id))
                paragraph_id += 1
                paragraph_lines = []  # Reset for the next paragraph

            # Increment page_id after every 'rows_per_page' row
            if (index + 1) % rows_per_page == 0:
                current_page_id += 1

        return paragraphs
    
    def get_sheet_number(self):
        """
        Returns the number of sheets in the Excel file.
        
        Returns:
        int: The number of sheets in the Excel file.
        """
        return len(pd.ExcelFile(self.path).sheet_names)
    
    
