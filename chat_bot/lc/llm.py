from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI

chat = ChatOpenAI(temperature=0)
llm = OpenAI(temperature=0, streaming=True)