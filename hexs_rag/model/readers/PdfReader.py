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

from hexs_rag.model.model.paragraph import Paragraph
from hexs_rag.utils.model.pdfreader import *
from hexs_rag.utils.utils.table_converter import table_converter


class PdfReader:
    """
    A class for reading and parsing PDF files content. First it opens the PDF and extract the text and tables from the page. 
    It also detects images and extract the text from them. After getting the text from the page it creates the list of paragraphs.

    Attributes:
    path : str
        The path to the PDF file
    paragraphs : list[Paragraph]
        The list of paragraphs extracted from the PDF

    Methods:
    most_occuring_fonts(line_formats : list) -> list
        Returns the most occuring font sizes in the list of formats
    text_extraction(element) -> tuple
        Extracts the text from the in line text element
    extract_table(pdf_path, page_num, table_num) -> list
        Extracts the table from the page
    is_element_inside_any_table(element, page ,tables) -> bool
        Checks if the element is inside any table present in the page
    find_table_for_element(element, page ,tables) -> int
        Finds the table for a given element in the page
    crop_image(element, pageObj) -> None
        Crops the image from the PDF
    convert_to_images(input_file) -> None
        Converts the PDF to images
    image_to_text(image_path) -> str
        Reads text from images and returns it
    pdf_manager(pdf_path, actual_first_page=0, include_images=True) -> list
        This is the main method of the class. It manages the extraction of the text and tables from the PDF. 
        This is the method that finally creates the list of paragraphs. 
    """

    def __init__(self, path, actual_first_page_=0, include_images=True):
        self.path = path
        self.paragraphs = self.pdf_manager(
            path, actual_first_page_, include_images=include_images
        )

    def most_occuring_fonts(self, line_formats: list):
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

    def text_extraction(self, element):
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
        return (line_text, format_per_line)

    # Extracting tables from the page
    def extract_table(self, pdf_path, page_num, table_num):
        # Open the pdf file
        pdf = pdfp.open(pdf_path)
        # Find the examined page
        table_page = pdf.pages[page_num]
        # Extract the appropriate table
        table = table_page.extract_tables()[table_num]

        return table

    # Create a function to check if the element is in any tables present in the page
    def is_element_inside_any_table(self, element, page, tables):
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
        images = convert_from_path(input_file)
        image = images[0]
        output_file = "PDF_image.png"
        image.save(output_file, "PNG")

    # Create a function to read text from images
    def image_to_text(self, image_path):
        # Read the image
        img = Image.open(image_path)
        # Extract the text from the image
        text = pytesseract.image_to_string(img)
        return text

    def pdf_manager(self, pdf_path, actual_first_page=0, include_images=True):
        # create a PDF file object
        pdfFileObj = open(pdf_path, "rb")
        # create a PDF reader object
        pdfReaded = pypdf.PdfReader(pdfFileObj)
        number_of_pages = len(pdfReaded.pages)
        # Create the dictionary to extract text from each image
        text_per_page = {}
        # Create a boolean variable for image detection
        image_flag = False
        actual_first_page = int(actual_first_page)
        if actual_first_page > number_of_pages:
            page_numbers = None
        else:
            page_numbers = [i for i in range(actual_first_page - 1, number_of_pages)]
        # We extract the pages from the PDF
        for pagenum, page in enumerate(
            extract_pages(pdf_path, page_numbers=page_numbers)
        ):
            # Initialize the page object
            pagenum = page_numbers[pagenum] if page_numbers else pagenum
            pageObj = pdfReaded.pages[pagenum]
            # Initialize the variables needed for the text extraction from the page
            page_text = []
            line_format = []
            text_from_images = []
            text_from_tables = []
            page_content = []
            # Initialize the number of the examined tables
            table_in_page = -1
            # Open the pdf file
            pdf = pdfp.open(pdf_path)
            # Find the examined page
            page_tables = pdf.pages[pagenum]
            # Find the number of tables in the page

            tables = page_tables.find_tables()
            if len(tables) != 0:
                table_in_page = 0

            # Extracting the tables of the page
            for table_num in range(len(tables)):
                # Extract the information of the table
                table = self.extract_table(pdf_path, pagenum, table_num)
                # Convert the table information in structured string format
                table_string = table_converter(table)
                # Append the table string into a list
                text_from_tables.append(table_string)

            # Find all the elements
            page_elements = [(element.y1, element) for element in page._objs]
            # Sort all the element as they appear in the page
            page_elements.sort(key=lambda a: a[0], reverse=True)

            # Find the elements that composed a page
            for i, component in enumerate(page_elements):
                # Extract the element of the page layout
                element = component[1]

                # Check the elements for tables
                if table_in_page == -1:
                    pass
                else:
                    if self.is_element_inside_any_table(element, page, tables):
                        table_found = self.find_table_for_element(element, page, tables)
                        if table_found == table_in_page and table_found != None:
                            page_content.append(text_from_tables[table_in_page])
                            page_text.append("table")
                            line_format.append("table")
                            table_in_page += 1
                        # Pass this iteration because the content of this element was extracted from the tables
                        continue

                if not self.is_element_inside_any_table(element, page, tables):

                    # Check if the element is text element
                    if isinstance(element, LTTextContainer):
                        # Use the function to extract the text and format for each text element
                        (line_text, format_per_line) = self.text_extraction(element)
                        # Append the text of each line to the page text
                        page_text.append(line_text)
                        # Append the format for each line containing text
                        line_format.append(format_per_line)
                        page_content.append(line_text)

                    # Check the elements for images
                    if include_images:
                        if isinstance(element, LTFigure):
                            # Crop the image from PDF
                            self.crop_image(element, pageObj)
                            # Convert the croped pdf to image
                            self.convert_to_images("cropped_image.pdf")
                            # Extract the text from image
                            image_text = self.image_to_text("PDF_image.png")
                            text_from_images.append(image_text)
                            page_content.append(image_text)
                            # Add a placeholder in the text and format lists
                            page_text.append("image")
                            line_format.append("image")
                            # Update the flag for image detection
                            image_flag = True

            # Create the key of the dictionary
            dctkey = "Page_" + str(pagenum)
            # Add the list of list as value of the page key
            text_per_page[dctkey] = [
                page_text,
                line_format,
                text_from_images,
                text_from_tables,
                page_content,
            ]

        # Close the pdf file object
        pdfFileObj.close()

        # Create a list of formats for all the pages
        formats = []
        for p in text_per_page.values():
            formats.append(p[1])

        # flatten the list of lists
        formats = flatten(formats)

        # keep only the font sizes in the list
        formats = keep_int_and_floats_in_list(formats)

        # group the formats in lists of similar formats
        grouped_formats = group_formats(formats)

        # create a dictionary with the format as key and the style as value
        styles = create_dict_and_assign_styles_from_format(grouped_formats)

        # display the result on a separate file as a JSON with some indentation for better visualization
        with open(file="styles.txt", mode="a") as fp:
            if fp.tell() == 0:
                fp.write(
                    "Document title: " + pdf_path.split("/")[-1] + "\n"
                ) if "/" in pdf_path else fp.write(
                    "Document title: " + pdf_path.split("\\")[-1] + "\n"
                )
            else:
                fp.write(
                    "\nDocument title: " + pdf_path.split("/")[-1] + "\n"
                ) if "/" in pdf_path else fp.write(
                    "\nDocument title: " + pdf_path.split("\\")[-1] + "\n"
                )
            json.dump(styles, fp, indent=4)

        # Delete the additional files created if image is detected
        if image_flag:
            os.remove("cropped_image.pdf")
            os.remove("PDF_image.png")

        # beginning of the paragraph extraction
        paragraphs = []
        for index, page in enumerate(text_per_page.values()):
            content_format = page[1]
            j = 0
            while j + 1 < len(content_format):
                actual_format = content_format[j]
                n_of_fontsizes = len(
                    list(
                        i
                        for i in actual_format
                        if isinstance(i, int) or isinstance(i, float)
                    )
                )
                if n_of_fontsizes > 1:
                    actual_format = max(keep_int_and_floats_in_list(actual_format))
                    actual_format = find_good_key_in_dict(styles, actual_format)
                elif n_of_fontsizes == 1:
                    actual_format = keep_int_and_floats_in_list(actual_format)[0]
                    actual_format = find_good_key_in_dict(styles, actual_format)
                elif n_of_fontsizes == 0 and actual_format == "table":
                    actual_format = "table"
                else:
                    actual_format = "content"
                if len(page[4][j]) > 150 and "title" in actual_format:
                    actual_format = "content"

                # print(actual_format)
                paragraph = Paragraph(
                    text=page[4][j], font_style=actual_format, id_=j, page_id=index
                )
                paragraphs.append(paragraph)
                j += 1

        paragraphs = (
            self.concatenate_paragraphs(paragraphs, pdf_path.split("/")[-1])
            if "/" in pdf_path
            else self.concatenate_paragraphs(paragraphs, pdf_path.split("\\")[-1])
        )

        # print("@*"*50)
        # for paragraph in paragraphs:
        # print(f"Level: {paragraph.level}, Font Style: {paragraph.font_style}")
        # print("@*"*50)

        return paragraphs

    def concatenate_paragraphs(self, paragraphs, doc_title):
        concatenated_paragraphs = []
        i = 0
        actual_page_id = paragraphs[0].page_id
        while i < len(paragraphs):
            p = paragraphs[i]
            if (
                p.blank
                or "REST API Developer Guide 23.3" in p.text
                or "x! illumio" in p.text
            ):
                i += 1
                continue
            if (
                (p.page_id != actual_page_id)
                and doc_title == "Illumio_Core_REST_API_Developer_Guide_23.3.pdf"
                and (not p.font_style == "table" and not "title" in p.font_style)
            ):
                i += 2
                actual_page_id = p.page_id
                continue
            if not concatenated_paragraphs:
                concatenated_paragraphs.append(p)
            elif p.font_style != concatenated_paragraphs[-1].font_style:
                if (
                    p.font_style == "table"
                    and concatenated_paragraphs[-1].font_style == "content"
                ) or (
                    p.font_style == "content"
                    and concatenated_paragraphs[-1].font_style == "table"
                ):
                    concatenated_paragraphs[-1].text += "\n" + p.text
                else:
                    concatenated_paragraphs.append(p)
            else:
                if "title" in p.font_style:
                    concatenated_paragraphs[-1].text += " : " + p.text
                    concatenated_paragraphs[-1].text = (
                        concatenated_paragraphs[-1]
                        .text.replace("\n", "")
                        .replace("\r", "")
                    )
                else:
                    concatenated_paragraphs[-1].text += "\n" + p.text
            i += 1
        return concatenated_paragraphs

    # TODO del if never used?
    def rearrange_paragraphs(self, paragraphs: list[Paragraph]):
        # associate paragraphs with the same font style
        i = 0
        while i < len(paragraphs):
            paragraphs[i] = paragraphs[i].rearrange()
            i += 1
        return paragraphs
