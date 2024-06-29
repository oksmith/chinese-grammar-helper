from typing import Dict, List

from dotenv import load_dotenv

from langchain_astradb.vectorstores import AstraDBVectorStore
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.runnables.base import Runnable
from langchain_core.documents import Document
from langchain.prompts.chat import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()


def get_agent(vector_store: AstraDBVectorStore) -> Runnable:
    """
    Create the main RAG agent for answering questions about Chinese
    grammar.
    """
    # Define the retriever using our vector database
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

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
    return rag_chain


def format_docs(docs: List[Document]) -> str:
    output = "\n\n".join([doc.page_content for doc in docs])
    output += "\n\nThe following URLs contain more information and explanation:"
    output += "\n*".join([doc.metadata["url"] for doc in docs])
    return output


def format_output(result: Dict) -> str:
    output = f"\nAnswer: {result['answer']}\n\n"
    output += "For links to more information, see the following:\n* "
    output += "\n* ".join([d.metadata["url"] for d in result["context"]])
    return output
