from typing import Dict, List

from dotenv import load_dotenv
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts.chat import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI

from src.data import load_data
from src.vectorstore.database import connect_to_vector_store

load_dotenv()


def format_docs(docs: List[Document]) -> str:
    output = "\n\n".join([doc.page_content for doc in docs])
    output += "\n\nThe following URLs contain more information and explanation:"
    output += "\n*".join([doc.metadata["url"] for doc in docs])
    return output


def format_output(result: Dict) -> str:
    output = f"\nAnswer: {result['answer']}\n\n"
    output += "For links to more information, see the following:\n* "
    output += "\n* ".join([d.metadata['url'] for d in result['context']])
    return output


if __name__ == "__main__":
    astra_db_store = connect_to_vector_store()
    
    recreate = input("Recreate vector database? (y/N) ").lower() in ["y", "yes"]
    if recreate:
        try:
            astra_db_store.delete_collection()
        except:  # noqa: E722
            pass

        # Load document and split it into several nodes
        documents = load_data.get_web_data()

        astra_db_store = connect_to_vector_store()
        print(f"LENGTH OF DOCUMENTS: {len(documents)}")
        print(f"Example document: {documents[5]}\n\n")

        astra_db_store.add_documents(documents)

        # verify a search
        results = astra_db_store.similarity_search("了", k=3)
        for result in results:
            print(f"* {result.page_content} {result.metadata} \n\n")

    # Define the retriever using our vector database
    retriever = astra_db_store.as_retriever(search_kwargs={"k": 3})

    # Initialise LLM
    llm = ChatOpenAI(model="gpt-3.5-turbo-1106")

    # Incorporate the retriever into a question-answering chain
    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Use five sentences maximum and keep the "
        "answer concise."
        "\n\n"
        "{context}"
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    # rag_chain = (
    #     {"context": retriever | format_docs, "question": RunnablePassthrough()}
    #     | prompt
    #     | llm
    #     | StrOutputParser()
    # )

    while (question := input("Ask a question about Chinese grammar (q to quit): ")) != "q":
        # example: How should I use 竟然?
        # example: How should I use 刚 and 了 in the same sentence?
        # result = rag_chain.invoke(question)
        result = rag_chain.invoke({"input": question})
        print(format_output(result))

    print("Exiting program.")
