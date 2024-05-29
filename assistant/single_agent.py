from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

from assistant.llm_provider.openai.gpt import CHAT
from assistant.tools.researcher.serpapi import serp_search_tool
from assistant.tools.researcher.wikipedia import wiki_search_tool
from assistant.tools.math.calculator import calculator_tool


# Adapted from https://smith.langchain.com/hub/hwchase17/openai-tools-agent
openai_tools_prompt = ChatPromptTemplate.from_messages(
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

# set tools
tools = [
    serp_search_tool,
    wiki_search_tool,
    calculator_tool,
]

# openai agent(BUG：如果用中转api, 这里就会报错，还不知道是什么原因)
agent = create_openai_tools_agent(CHAT, tools, openai_tools_prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, )

chain_with_history = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: msgs,
    input_messages_key="input",
    output_messages_key="output",
    history_messages_key="history",
)