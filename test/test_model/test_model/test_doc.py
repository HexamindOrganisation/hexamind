from hexs_rag.model.model.doc import Doc
import pytest


class TestDoc:
    def test_excel_read(doc_excel_instance):
        assert doc_excel_instance is not None

    def test_html_read(doc_html_instance):
        assert doc_html_instance is not None

    def test_pdf_read(doc_pdf_instance):
        assert doc_pdf_instance is not None

    def test_word_read(doc_word_instance):
        for block in doc_word_instance.blocks:
            assert block.context is not None