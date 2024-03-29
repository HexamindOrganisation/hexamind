from hxm_rag.model.modelv2.document import Document
from hxm_rag.model.modelv2.container import Container
from hxm_rag.model.modelv2.block import Block
from hxm_rag.model.readersv2.PdfReader import PdfReader
from hxm_rag.model.readersv2.WordReader import WordReader

if __name__ == "__main__":
    doc = WordReader('data/SGFGAS/Epargne-logement phase épargne.docx')