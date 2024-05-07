import os

from dotenv import find_dotenv, load_dotenv
from langchain_community.chat_models import ChatOpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

chat_model = ChatOpenAI(openai_api_key=api_key, model="gpt-3.5-turbo-1106")

result = chat_model.invoke("hello there")
print(result)
# content = 'Hello! How can I assist you today?' 
# response_metadata = {
#     'token_usage': {
#         'completion_tokens': 9,
#         'prompt_tokens': 9,
#         'total_tokens': 18
#     },
#     'model_name': 'gpt-3.5-turbo-1106',
#     'system_fingerprint': None,
#     'finish_reason': 'stop',
#     'logprobs': None
# }
# id = 'run-3534bdd6-92ca-4beb-a5d4-68ddfb5704e2-0'

result = chat_model.invoke("Do you speak 中文?")
print(result)
# content = 'Yes, I can understand and communicate in 中文 (Chinese). If you have any questions or need assistance in 中文, feel free to ask!' 
# response_metadata = {
#     'token_usage': {
#         'completion_tokens': 30,
#         'prompt_tokens': 13,
#         'total_tokens': 43
#     },
#     'model_name': 'gpt-3.5-turbo-1106',
#     'system_fingerprint': None,
#     'finish_reason': 'stop',
#     'logprobs': None
# }
# id = 'run-663d67d8-1dd3-40e1-9611-c5a2eeb1b7cc-0'
