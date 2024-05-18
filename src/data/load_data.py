import os 

from llama_index.core import StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.readers.file import PDFReader


PDF_PATH = os.path.join("data", "chinese_grammar_textbook", "ModernMandarinChineseGrammar_Textbook.pdf")


def get_index(data, index_name):
    index = None
    if not os.path.exists(index_name):
        print(f"building index {index_name}")
        index = VectorStoreIndex.from_documents(data, show_progress=True)
        index.storage_context.persist(persist_dir=index_name)
    else:
        index = load_index_from_storage(StorageContext.from_defaults(persist_dir=index_name))

def get_pdf_engine(path: str, name: str) -> VectorStoreIndex:
    pdf = PDFReader().load_data(path)
    index = get_index(pdf, name)
    engine = index.as_query_engine()
    return engine
