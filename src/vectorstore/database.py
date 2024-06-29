import os

from typing import List

from dotenv import load_dotenv
from langchain_astradb.vectorstores import AstraDBVectorStore
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

from src.logging import get_logger

load_dotenv()


def connect_to_vector_store() -> AstraDBVectorStore:
    # TODO: does there exist a better embedding model to use for multilingual
    # sentences (mostly English with some Mandarin)?
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    
    # load database endpoint variables
    db_endpoint = os.getenv("ASTRA_DB_API_ENDPOINT")
    token = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
    namespace = None

    astra_db = AstraDBVectorStore(
        embedding=embeddings,
        api_endpoint=db_endpoint,
        token=token,
        namespace=namespace,
        collection_name="chinese_grammar",
    )
    return astra_db


def load_documents_and_check(documents: List[Document]) -> AstraDBVectorStore:
    """
    Load vector store, add documents and return vector store.
    """
    astra_db_store = connect_to_vector_store()
    logger = get_logger()
    logger.info(f"LENGTH OF DOCUMENTS: {len(documents)}")
    logger.info(f"Example document: {documents[5]}\n\n")

    astra_db_store.add_documents(documents)

    # verify a search
    results = astra_db_store.similarity_search("了", k=3)
    for result in results:
        logger.info(f"* {result.page_content} {result.metadata} \n\n")

    return astra_db_store
