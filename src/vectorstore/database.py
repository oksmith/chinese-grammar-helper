from logging import Logger
from typing import List

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

from src.data import load_data

load_dotenv()


def connect_to_vector_store(logger: Logger) -> QdrantVectorStore:
    # TODO: does there exist a better embedding model to use for multilingual
    # sentences (mostly English with some Mandarin)? Or for Q&A retrieval tasks?
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

    client = QdrantClient(path="./vectorstore")
    collection_name = "chinese_grammar"

    try:
        # Check if the collection exists
        client.get_collection(collection_name)
        logger.info(
            f"Collection '{collection_name}' already exists, loading from disk."
        )
    except ValueError:
        client.create_collection(
            collection_name=collection_name,
            # text-embedding-ada-002 produces 1536-dim
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
        )

    vector_store = QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=embeddings,
    )

    return vector_store


def create_vector_store(logger: Logger) -> QdrantVectorStore:
    # Load document and split it into several nodes
    documents = load_data.get_web_data(path=load_data.WEB_PATH, logger=logger)
    if len(documents) == 0:
        logger.warn(
            "No documents found in the data directory, cannot create the database."
        )
    else:
        # reload fresh vector store and add documents
        vector_store = load_documents_and_check(documents, logger=logger)
        logger.info("Updated the vector database.")

    return vector_store


def load_documents_and_check(
    documents: List[Document], logger: Logger
) -> QdrantVectorStore:
    """
    Load vector store, add documents and return vector store.
    """
    vector_store = connect_to_vector_store(logger)
    logger.debug(f"LENGTH OF DOCUMENTS: {len(documents)}")
    logger.debug(f"Example document: {documents[5]}\n\n")

    # TODO: how to add documents to Qdrant vector store
    vector_store.add_documents(documents)
    # vector_store.add_documents(documents=documents, ids=uuids)

    # verify a search
    results = vector_store.similarity_search("了", k=3)
    for result in results:
        logger.debug(f"* {result.page_content} {result.metadata} \n\n")

    return vector_store
