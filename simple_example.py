import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain.schema import BaseOutputParser, HumanMessage

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

chat_model = ChatOpenAI(openai_api_key=api_key, model="gpt-3.5-turbo-1106")


# # Simple example invoking GPT-3.5

# result = chat_model.invoke("Do you speak 中文?")
# print(result)
# # content = 'Yes, I can understand and communicate in 中文 (Chinese). If you have any questions or need assistance in 中文, feel free to ask!' 
# # response_metadata = {
# #     'token_usage': {
# #         'completion_tokens': 30,
# #         'prompt_tokens': 13,
# #         'total_tokens': 43
# #     },
# #     'model_name': 'gpt-3.5-turbo-1106',
# #     'system_fingerprint': None,
# #     'finish_reason': 'stop',
# #     'logprobs': None
# # }
# # id = 'run-663d67d8-1dd3-40e1-9611-c5a2eeb1b7cc-0'



# # Pass in multiple messages, and get a single response from the combination of all of them

# messages = [
#     HumanMessage(content="My Chinese name is 欧立 please call me that when responding to my questions about Chinese"),
#     HumanMessage(content="What is my name?"),
#     HumanMessage(content="How do you pronounce my name?"),
# ]

# result = chat_model.predict_messages(messages=messages)
# print(result.content)
# # Your Chinese name, 欧立, is pronounced as "Ōu lì" in Mandarin. The first syllable 
# # "Ōu" is pronounced as "oh" with a rising tone, and the second syllable "lì" is
# # pronounced as "lee" with a falling tone.



# # parsing the output

class OutputParser(BaseOutputParser):
    def parse(self, text: str) -> str:
        """ Parse the output of an LLM call. """
        return text.strip().split(". ")
    


# Prompt templates 

system_template = "You are a helpful assistant who translates {input_language} into {output_language}. Reply in English."
human_template = "{text}"

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("system", "Make sure you reply in English!"),  # without this additional system prompt, it initially replied in Cbinese
    ("human", human_template)
])

messages = chat_prompt.format_messages(
    input_language="Chinese",
    output_language="English",
    text="数据科学家是做什么的？",  # what does a data scientist do?
)
# result = chat_model.predict_messages(messages=messages)
# print(result.content)
# # A data scientist is responsible for collecting, analyzing, and interpreting large sets of data to help
# # organizations make informed decisions. They use their expertise in statistics, programming, and machine
# # learning to extract valuable insights from data and develop predictive models. Data scientists are also
# # proficient in data visualization and communication, as they often need to present their findings to
# # non-technical audiences.
# # # NOTE: this was the first output. I had to add an additional system prompt to tell it to reply in English.
# # 数据科学家主要负责从结构化和非结构化数据中提取信息，分析数据模式和趋势，并为企业做出数据驱动的决策。他们使用统计学、
# # 机器学习和编程技能来处理大量数据，并通过可视化和报告将分析结果传达给非技术人员。数据科学家还可能参与数据收集和清洗，
# # 并开发预测模型和算法来解决实际业务问题。


# parsed = OutputParser().parse(result.content)
# steps, answer = parsed 
# print(answer)

chain = chat_prompt | chat_model | OutputParser()

# result = chain.invoke({"input_language": "Chinese", "output_language": "English", "text": "分析是什么？"})
# print(result)
# # [
# #     'Analysis is the process of examining something in detail in order to understand its nature, structure, or functioning', 
# #     'It involves breaking down a complex topic into smaller parts and examining how they relate to each other.'
# # ]
