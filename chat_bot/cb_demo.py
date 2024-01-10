
from langchain import hub
from langchain.agents import create_react_agent, initialize_agent, AgentType, AgentExecutor
from chat_bot.lc.llm import llm
from chat_bot.lc.tool import tools
from chat_bot.lc.RAG import configure_retriever, PrintRetrievalHandler, StreamHandler
from chat_bot.lc.db import LOCALDB, INJECTION_WARNING, create_agent_db_from_url



# Initialize agent
react_agent = create_react_agent(llm, tools, hub.pull("hwchase17/react"))
agent_ = initialize_agent(tools=tools, llm=llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
mrkl = AgentExecutor(agent=react_agent, tools=tools)

# Initialize agent_db

from langchain_openai import ChatOpenAI
chat = ChatOpenAI(temperature=0)




