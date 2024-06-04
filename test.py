from hxm_rag.model.model.document import Document
from hxm_rag.model.model.container import Container
from hxm_rag.model.model.block import Block
from hxm_rag.model.readers.WordReader import WordReader

if __name__ == "__main__":
    doc = WordReader('data/SGFGAS/Epargne-logement phase épargne.docx')