import os

from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI

api_key = os.environ["OPENAI_API_KEY"]
base_url = os.environ.get("OPENAI_API_BASE", None)

chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, api_key=api_key, base_url=base_url)
llm = OpenAI(model="gpt-3.5-turbo", temperature=0, streaming=True, api_key=api_key, base_url=base_url)

# chat_qianfan =