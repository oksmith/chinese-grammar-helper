import os

from dotenv import load_dotenv
from langchain_astradb.vectorstores import AstraDBVectorStore
from langchain_openai import OpenAIEmbeddings

load_dotenv()


def connect_to_vector_store() -> AstraDBVectorStore:
    # intialise embeddings
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