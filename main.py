#!/usr/bin/env python
import click

from src.logging import get_logger
from src.rag import rag
from src.vectorstore import database


@click.group()
def cli():
    pass


@click.command()
def updatedb():
    logger = get_logger()
    database.create_vector_store(logger)


@click.command()
@click.option(
    "--updatedb",
    is_flag=True,
    default=False,
    help="If set, include prompting to allow user to update the vector database.",
)
def helper(updatedb):
    logger = get_logger()

    logger.info("Loading embeddings, connecting to vector store...")
    astra_db_store = database.connect_to_vector_store(logger)
    if updatedb:
        recreate = input("Recreate vector database? (y/N) ").lower() in ["y", "yes"]
        if recreate:
            astra_db_store = database.create_vector_store(logger=logger)

    logger.info("Loading RAG agent...")
    rag_chain = rag.get_agent(astra_db_store)

    while (
        question := input("Ask a question about Chinese grammar (q to quit): ")
    ) != "q":
        if question.strip("\n").strip(" ").strip("\t") == "":
            continue

        # example: How should I use 竟然?
        # example: How should I use 刚 and 了 in the same sentence?
        # result = rag_chain.invoke(question)
        result = rag_chain.invoke({"input": question})

        # Use stdout without logger for the agent output
        print(rag.format_output(result))

    logger.info("Exiting program.")


cli.add_command(updatedb)
cli.add_command(helper)

if __name__ == "__main__":
    cli()
