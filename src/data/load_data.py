import json
import os
from typing import List

from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.documents import Document

load_dotenv()

PDF_PATH = os.path.join("data", "chinese_grammar_textbook", "ModernMandarinChineseGrammar_Textbook.pdf")
WEB_PATH = os.path.join("data", "chinese_grammar_data")
METADATA_PATH = os.path.join("data", "metadata.json")


# def get_pdf_data(file_path=PDF_PATH):
#     # configure global settings for Llamaindex
#     Settings.llm = OpenAI(model="gpt-3.5-turbo-1106")
#     Settings.embed_model = OpenAIEmbedding(
#         model="text-embedding-ada-002", embed_batch_size=100
#     )

#     # load pdf documents
#     documents = LlamaParse(result_type="text").load_data(file_path)
#     return documents

# def documents_to_nodes(documents):
#     # parse documents into nodes
#     node_parser = SimpleNodeParser()
#     nodes = node_parser.get_nodes_from_documents(documents)

#     return nodes

def get_web_data(path: str = WEB_PATH) -> List[Document]:
    documents = DirectoryLoader(path, glob="**/*.txt", loader_cls=TextLoader, show_progress=True).load()

    with open(METADATA_PATH, "r") as f:
        overall_metadata = json.load(f)
    
    documents = [
        Document(page_content=doc.page_content, metadata={"url": overall_metadata[doc.metadata["source"].split("/")[-1].split(".")[0]]["url"]})
        for doc in documents
    ]
    return documents
