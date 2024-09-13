from collections import Counter
from hexamind.model.readers.IReader import IReader
from PIL import Image
from hexamind.utils.logger import logger
import logging
import fitz
import html
import numpy as np
import pytesseract
import io
import os

logger = logger(log_file='my_app.log', log_level=logging.DEBUG)


class PdfReader(IReader):

    def __init__(self, path: str):

        self.pdf_path = path
        self.temp_path = "temp.pdf"

        self.folder_path = os.path.join("./hexamind/model/readers/", self.pdf_path.replace(" ", "_")+"_images")
        

        self.html_path = "PdfReader.html"
        doc = fitz.open(self.pdf_path)
        doc.save(self.temp_path)
        doc.close()

        #self.convert_to_html()
        

    def convert_to_htlm(self) -> str:
        pdf_text_data = self.pdf_text_data()
        sorted_sizes, most_common_size = self.font_list_def(pdf_text_data)

        n = 0
        while len(sorted_sizes) > 7:
            n += 0.01
            sorted_sizes = self.aggregate_by_largest(sorted_sizes, n)
            pdf_text_data = self.font_re_mapping(pdf_text_data, sorted_sizes)
            sorted_sizes, most_common_size = self.font_list_def(pdf_text_data)
            for size in sorted_sizes:
                if size < most_common_size:
                    sorted_sizes.remove(size)

        pdf_text_data = self.font_re_mapping(pdf_text_data, sorted_sizes)


        html_content = "<html><body>"

        for text, size in pdf_text_data:
            if size <= most_common_size:
                html_content += f"<p>{html.escape(text)}</p>"

            else:
                if sorted_sizes[0] <= size <= sorted_sizes[0]:
                    html_content += f"<h1>{html.escape(text)}</h1>"
                elif size == sorted_sizes[1]:
                    html_content += f"<h2>{html.escape(text)}</h2>"
                elif size == sorted_sizes[2]:
                    html_content += f"<h3>{html.escape(text)}</h3>"
                elif size == sorted_sizes[3]:
                    html_content += f"<h4>{html.escape(text)}</h4>"
                elif size == sorted_sizes[4]:
                    html_content += f"<h5>{html.escape(text)}</h5>"
                elif size == sorted_sizes[5]:
                    html_content += f"<h6>{html.escape(text)}</h6>"
                else:
                    html_content += f"<h6>{html.escape(text)}</h6>"

        html_content += "</body></html>"

        remove = ["</p><p>", "</h1><h1>", "</h2><h2>", "</h3><h3>", "</h4><h4>", "</h5><h5>", "</h6><h6>"]
        html_content = html_content.replace(remove[1], " ").replace(remove[2], " ").replace(remove[3], " ")
        html_content = html_content.replace(remove[4], " ").replace(remove[5], " ").replace(remove[6], " ")
        html_content = html_content.replace(remove[0], " ")
        replace = ["&quot;", "<p>&lt;", "&lt;", "&gt;</p>", "&gt;"]
        html_content = html_content.replace(replace[0], '"')
        html_content = html_content.replace(replace[1], "<").replace(replace[2], "<")
        html_content = html_content.replace(replace[3], ">").replace(replace[4], ">")

        # Write HTML content to file with utf-8-sig encoding
        # with open(self.html_path, 'w', encoding='utf-8-sig') as html_file:
        #    html_file.write(html_content)
        return html_content

    def pdf_text_data(self):

        
        if 0:
            os.makedirs(self.folder_path, exist_ok=True)
            self.image_tag_and_save_to_file()

        doc = fitz.open(self.temp_path)

        sentences = []

        for page in doc:
            text_blocks = page.get_text("dict")["blocks"]
            for block in text_blocks:
                if block["type"] == 0:  # text block
                    for line in block["lines"]:
                        spans = line["spans"]
                        if not spans:
                            continue

                        for span in spans:
                            sentence_text = span["text"]
                            font_sizes = span["size"]

                            if span["flags"] & 16 ** 1:
                                font_sizes += .1

                            elif span["flags"] & 2 ** 1:
                                font_sizes += .05

                            if font_sizes:
                                min_font_size = font_sizes
                            else:
                                min_font_size = 0.001
                            sentences.append([sentence_text, min_font_size])

        return sentences

    # This method is now deprecated but is used to extract images' text
    def image_text_data(self):
        doc = fitz.open(self.temp_path)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            image_list = page.get_images(full=True)

            # Iterate over images in the page
            for img_index, img in enumerate(image_list):
                try:
                    xref = img[0]

                    # Extract image bytes
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]

                    image = Image.open(io.BytesIO(image_bytes))
                    # Enlarge the image before OCR
                    scale_factor = 5  # Factor by which to enlarge the image
                    enlarged_image = image.resize(
                        (image.width * scale_factor, image.height * scale_factor),
                        Image.Resampling.LANCZOS
                    )
                    # Use pytesseract to extract text from the image
                    text = pytesseract.image_to_string(enlarged_image)

                    for block in page.get_text("dict")["blocks"]:
                        if block["type"] == 1:  # Image block
                            block_rect = fitz.Rect(block["bbox"])

                            page.draw_rect(block_rect, color=(1, 1, 1), fill=(.5, .5, .5))

                            # Insert the extracted text at the location of the image
                            page.insert_textbox(block_rect, text, fontsize=1, color=(0, 0, 0))

                except Exception as e:
                    logger.log(f"An error occurred on page {page_num}: {e}", logging.WARNING)
            logger.log(f"Processed page {page_num + 1}/{len(doc)}", logging.INFO)
        doc.saveIncr()
        doc.close()

    def image_tag_and_save_to_file(self):
        doc = fitz.open(self.temp_path)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            image_list = page.get_images(full=True)

            # Iterate over images in the page
            for img_index, img in enumerate(image_list):
                try:
                    xref = img[0]  # The XREF of the image
                    base_image = doc.extract_image(xref)  # Extract image data

                    # Extract the image bytes, type, and extension
                    img_bytes = base_image["image"]
                    img_ext = base_image["ext"]

                    # Create the image file name
                    img_filename = f"page_{page_num + 1}_img_{img_index + 1}.{img_ext}"
                    img_path = self.folder_path + "/" + img_filename
                    print(img_path)
                    # Save the image to the specified directory
                    with open(img_path, "wb") as img_file:
                        img_file.write(img_bytes)

                    text = '<img class="fit-picture"src='+img_path+' alt=""/>'

                    print(text)
                    for block in page.get_text("dict")["blocks"]:
                        if block["type"] == 1:  # Image block
                            block_rect = fitz.Rect(block["bbox"])
                            page.insert_textbox(block_rect, text, fontsize=1, color=(0, 0, 0))

                except Exception as e:
                    logger.log(f"An error occurred on page {page_num}: {e}", logging.WARNING)
            logger.log(f"Processed page {page_num + 1}/{len(doc)}", logging.INFO)
        doc.saveIncr()
        doc.close()

    @staticmethod
    def font_list_def(data, var=45):
        font_sizes = [item[1] for item in data]

        # Count occurrences of each font size
        size_counts = Counter(font_sizes)

        # Calculate total number of items
        total_count = len(font_sizes)

        # Calculate percentages
        percentages = {size: (count / total_count) * 100 for size, count in size_counts.items()}

        # Sort font sizes by size (largest to smallest)
        sorted_sizes = sorted(size_counts.keys(), reverse=True)

        # Find the most common font size
        most_common_size = size_counts.most_common(1)[0][0]
        first_common_size = None

        # Print the percentages
        logger.log("Font sizes sorted from largest to smallest with their percentages:", logging.INFO)
        for size in sorted_sizes:
            percentage = percentages[size]
            logger.log(f"Font size {size}: {percentage:.2f}%", logging.INFO)

            if first_common_size is None and percentage > var:
                first_common_size = size

        if first_common_size is not None:
            for digit in data:
                if digit[1] < first_common_size:
                    digit[1] = first_common_size

        # Print the most common font size
        logger.log(f"Most common font size: {most_common_size}", logging.INFO)
        logger.log(f"first common font size: {first_common_size}", logging.INFO)
        # Print the first common size with percentage greater than var

        body_size = most_common_size
        if first_common_size is not None and first_common_size > most_common_size:
            body_size = first_common_size

        return sorted_sizes, body_size  # , most_common_size

    @staticmethod
    def aggregate_by_largest(sorted_sizes, threshold=None):
        if not sorted_sizes:
            return []

        if threshold is None:
            std_dev = np.std(sorted_sizes)
            threshold = (max(sorted_sizes) - min(sorted_sizes)) / (7 * std_dev)

        result = [sorted_sizes[0]]
        current_min = sorted_sizes[0]

        for num in sorted_sizes[1:]:
            if num < current_min - threshold:  # Adjust comparison for descending order
                result.append(num)
            current_min = num

        return result

    @staticmethod  # This method is now deprecated
    def font_list_aggregation_incr(sorted_sizes, loop=-1, var=.01):
        # Create a mapping of old sizes to new aggregated sizes
        varInc = var
        new_sorted_sizes = sorted_sizes.copy()
        bool_sorted_sizes = [True] * len(sorted_sizes)
        check = True
        while check and loop != 0:
            loop -= 1
            for i in range(len(sorted_sizes)):
                if bool_sorted_sizes[i]:
                    bool_sorted_sizes[i] = False
                    index = i + 1

                    while index <= len(sorted_sizes) - 1 and new_sorted_sizes[index] >= new_sorted_sizes[i] - var:
                        new_sorted_sizes[index] = new_sorted_sizes[i]
                        index += 1
            var += varInc

            bool_sorted_sizes = [True] * len(sorted_sizes)
            if len(set(new_sorted_sizes)) <= 7 or var >= 5:
                check = False

        result = list(set(new_sorted_sizes))
        result.reverse()

        return result

    @staticmethod  # This method is now deprecated
    def aggregate_by_percent(data):
        font_sizes = [item[1] for item in data]

        # Count occurrences of each font size
        size_counts = Counter(font_sizes)

        # Calculate total number of items
        total_count = len(font_sizes)

        # Calculate percentages
        percentages = {size: (count / total_count) * 100 for size, count in size_counts.items()}

        # Sort font sizes by size (largest to smallest)
        sorted_sizes = sorted(size_counts.keys(), reverse=True)

        # Print the percentages
        logger.log("Font sizes sorted from largest to smallest with their percentages:", logging.INFO)
        for size in sorted_sizes:
            percentage = percentages[size]
            logger.log(f"Font size {size}: {percentage:.2f}%", logging.INFO)
            if percentage < 0.031 and size != max(sorted_sizes):
                sorted_sizes.remove(size)

        return sorted_sizes

    @staticmethod
    def font_re_mapping(data, sizes):
        temp_data = data.copy()
        temp_sizes = sizes.copy()

        def find_closest_larger(target):
            for num in temp_sizes:
                if num <= target:
                    return num
            return 1  # temp_sizes[-1]

        for digit in temp_data:
            new_digit = find_closest_larger(digit[1])
            digit[1] = new_digit

        return temp_data
