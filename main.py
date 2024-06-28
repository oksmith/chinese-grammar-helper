import os

from dotenv import load_dotenv

from langchain.prompts.chat import ChatPromptTemplate
from langchain.schema import BaseOutputParser
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.llms import openai
from langchain_openai import ChatOpenAI

from src.data import load_data, prompts

load_dotenv()


class OutputParser(BaseOutputParser):
    def parse(self, text: str) -> str:
        """ Parse the output of an LLM call. """
        return text.strip().split(". ")

if __name__ == "__main__":
    # TODO: link up to the PDF engine
    tools = [
        QueryEngineTool(
            query_engine=load_data.get_pdf_engine,
            metadata=ToolMetadata(
                name="textbook",
                description="This is a Chinese grammar textbook."
            )
        )
    ]

    model = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), model="gpt-3.5-turbo-1106")

    human_template = "{text}"
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant who notices unnatural sounding Chinese sentences and corrects them."),
        ("system", "Reply in Chinese correcting the sentence."),
        ("system", "Explain why it is not correct."),
        ("human", human_template)
    ])
    
    chain = chat_prompt | model | OutputParser()
    result = chain.invoke({"input_language": "Chinese", "output_language": "English", "text": "Correct my grammar: 我学习中文已经五年"})
    print(result)
