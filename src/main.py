import os

from dotenv import load_dotenv

from llama_index.core.agent import ReActAgent
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.llms import openai

from src.data import load_data, prompts

load_dotenv()

if __name__ == "__main__":
    print("in main")

    tools = [
        QueryEngineTool(
            query_engine=load_data.get_pdf_engine,
            metadata=ToolMetadata(
                name="textbook",
                description="This is a Chinese grammar textbook."
            )
        )
    ]

    model = openai.OpenAI(model="gpt-3.5-turbo-1106", openai_api_key=os.getenv("OPENAI_API_KEY"))
    agent = ReActAgent.from_tools(tools, llm=model, verbose=True, 
                                #   context=context
                                )

    