import click

from src.data import load_data
from src.logging import get_logger
from src.rag import rag
from src.vectorstore.database import connect_to_vector_store, load_documents_and_check


if __name__ == "__main__":
    astra_db_store = connect_to_vector_store()
    logger = get_logger()
    
    recreate = input("Recreate vector database? (y/N) ").lower() in ["y", "yes"]
    if recreate:
        try:
            astra_db_store.delete_collection()
        except:  # noqa: E722
            pass

        # Load document and split it into several nodes
        documents = load_data.get_web_data()

        # reload fresh vector store and add documents
        astra_db_store = load_documents_and_check(documents)

    rag_chain = rag.get_agent(astra_db_store)

    while (question := input("Ask a question about Chinese grammar (q to quit): ")) != "q":
        # example: How should I use 竟然?
        # example: How should I use 刚 and 了 in the same sentence?
        # result = rag_chain.invoke(question)
        result = rag_chain.invoke({"input": question})
        
        # Use stdout without logger for the agent output
        print(rag.format_output(result))

    logger.info("Exiting program.")
