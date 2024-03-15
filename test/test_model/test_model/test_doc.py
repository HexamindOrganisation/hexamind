# Description: Testing suite made for doc class. 
# Instances are defined by fixtures in conftest.py

from hxm_rag.model.model.doc import Doc
import pytest

# test that the instances work --> can be deleted later (just for test/debug setup)
def test_excel_read(doc_excel_instance):
    assert doc_excel_instance is not None

def test_html_read(doc_html_instance):
    assert doc_html_instance is not None

def test_pdf_read(doc_pdf_instance):
    assert doc_pdf_instance is not None

def test_word_read(doc_word_instance):
    assert doc_word_instance is not None
##########################################
# test initialisation (using objects created in conftest)

def test_excel_initialisation(doc_excel_instance):
    assert doc_excel_instance.title == 'SampleData', "Title should be filename minus extension"
    assert doc_excel_instance.extension == '.xlsx', "Extension should be one of the supported formats"
    assert isinstance(doc_excel_instance.id_, int), "ID should be an integer"
    assert doc_excel_instance.path == "../hexs_rag/data/test_data/SampleData.xlsx", "Path should match the input"
    assert doc_excel_instance.sheet_name == 0, "Sheet name should match the input"

def test_html_initialisation(doc_html_instance):
    assert doc_html_instance.title == 'HTML5 Test Page', "Title should be filename minus extension"
    assert doc_html_instance.extension == '.html', "Extension should be one of the supported formats"
    assert isinstance(doc_html_instance.id_, int), "ID should be an integer"
    assert doc_html_instance.path == "../hexs_rag/data/test_data/HTML5 Test Page.html", "Path should match the input"
    assert doc_html_instance.sheet_name == 0, "Sheet name should match the input"

def test_pdf_initialisation(doc_pdf_instance):
    assert doc_pdf_instance.title == 'pdf-test', "Title should be filename minus extension"
    assert doc_pdf_instance.extension == '.pdf', "Extension should be one of the supported formats"
    assert isinstance(doc_pdf_instance.id_, int), "ID should be an integer"
    assert doc_pdf_instance.path == "../hexs_rag/data/test_data/pdf-test.pdf", "Path should match the input"
    assert doc_pdf_instance.sheet_name == 0, "Sheet name should match the input"

def test_word_initialisation(doc_word_instance):
    assert doc_word_instance.title == 'sample_doc', "Title should be filename minus extension"
    assert doc_word_instance.extension == '.docx', "Extension should be one of the supported formats"
    assert isinstance(doc_word_instance.id_, int), "ID should be an integer"
    assert doc_word_instance.path == "../hexs_rag/data/test_data/sample_doc.docx", "Path should match the input"
    assert doc_word_instance.sheet_name == 0, "Sheet name should match the input"
###################################################

# test if blocks are being set correctly

def test_excel_blocks(doc_excel_instance):
    for block in doc_excel_instance.blocks:
        assert block.content is not None
        assert block.doc is not None
        assert block.index is not None
        assert type(block.doc) == str
        assert type(block.index) == str 
        assert type(block.content) == str


def test_html_blocks(doc_html_instance):
    for block in doc_html_instance.blocks:
        assert block.content is not None
        assert block.doc is not None
        assert block.index is not None
        assert type(block.doc) == str
        assert type(block.index) == str 
        assert type(block.content) == str

def test_pdf_blocks(doc_pdf_instance):
    for block in doc_pdf_instance.blocks:
        assert block.content is not None
        assert block.doc is not None
        assert block.index is not None
        assert type(block.doc) == str
        assert type(block.index) == str 
        assert type(block.content) == str

def test_word_blocks(doc_word_instance):
    for block in doc_word_instance.blocks:
        assert block.content is not None
        assert block.doc is not None
        assert block.index is not None
        assert type(block.doc) == str
        assert type(block.index) == str 
        assert type(block.content) == str

# check the content coming out
# def test_excel_block_content(doc_excel_instance):
#     assert doc_excel_instance.blocks[0].content == \
#     'SampleData/ :\n\n  Unnamed: 2: Online Instruction Page Unnamed: 2: Sample Data for Excel Unnamed: 2: Office Supply Sales Data  Unnamed: 2: Related tutorials Unnamed: 2: More Excel Sample Files Unnamed: 2: Named Excel Tables Unnamed: 2: Data Entry Tips  Unnamed: 2: Notes Unnamed: 1: • | Unnamed: 2: SalesOrders sheet has office supply sales data for a fictional company Unnamed: 1: • | Unnamed: 2: Each row represents an order.  Unnamed: 1: • | Unnamed: 2: The Total column could be changed to a formula, to multiply the Units and Cost columns.'

# def test_pdf_block_content(doc_pdf_instance):
#     assert doc_pdf_instance.blocks[0].content == \
#     'sample_doc/ :\n\nTemplate for Preparation of Papers for IEEE Sponsored Conferences & SymposiaFrank Anderson, Sam B. Niles, Jr., and Theodore C. Donald, Member, IEEEAbstract—These instructions give you guidelines for preparing papers for IEEE conferences. Use this document as a template if you are using Microsoft Word 6.0 or later. Otherwise, use this document as an instruction set. Instructions about final paper and figure submissions in this document are for IEEE journals; please use this document as a “template” to prepare your manuscript. For submission guidelines, follow instructions on paper submission system as well as the Conference website. Do not delete the blank line immediately above the abstract; it sets the footnote at the bottom of this column.'

# def test_html_block_content(doc_html_instance):
#     assert doc_html_instance.blocks[0].content == \

# def test_word_block_content(doc_word_instance):
#     assert doc_word_instance.blocks[0].content == \

###############################################
# test if paragraphs are being correctly set

# def test_excel_paragraph(doc_excel_instance):
#     assert doc_excel_instance.paragraphs[0] is not None
    

def test_word_paragraph(doc_word_instance):
    pass
##############################################################

# Test errors
def test_format_error():
    # make sure incorrect file format raises error
    with pytest.raises(ValueError):
        Doc(path="../hexs_rag/data/test_data/sample_txt.txt",
        include_images=True,
        actual_first_page=1)

################################################################
