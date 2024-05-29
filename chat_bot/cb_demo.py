from uuid import uuid4

from langchain import hub
from langchain.agents import create_react_agent, initialize_agent, AgentType, AgentExecutor, create_openai_tools_agent
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

from chat_bot.lc.llm import llm, chat
from chat_bot.lc.tool import tools
from chat_bot.lc.RAG import configure_retriever, PrintRetrievalHandler, StreamHandler
from chat_bot.lc.db import LOCALDB, INJECTION_WARNING, create_agent_db_from_url



# Initialize agent
react_agent = create_react_agent(llm, tools, hub.pull("hwchase17/react"))
agent_ = initialize_agent(tools=tools, llm=llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
mrkl = AgentExecutor(agent=react_agent, tools=tools)

# Initialize agent_db


# Adapted from https://smith.langchain.com/hub/hwchase17/openai-tools-agent
prompt_ = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. You may not need to use tools for every query - the user may just want to "
            "chat! But when they ask you about something that happened in real life, you may need to use tools to "
            "ensure that your answers are accurate."
            # "There are also some tools related to Gmail that allow you to view "
            # "Gmail information or send an email. Generally, you do not need to use these tools, but when users want "
            # "to process emails, you need to use them correctly."
            ,
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

# Set up memory
msgs = StreamlitChatMessageHistory(key="langchain_messages")
if len(msgs.messages) == 0:
    msgs.add_ai_message("How can I help you?")

agent = create_openai_tools_agent(chat, tools, prompt_)
agent_executor = AgentExecutor(agent=agent, tools=tools, )

chain_with_history = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: msgs,
    input_messages_key="input",
    output_messages_key="output",
    history_messages_key="history",
)

