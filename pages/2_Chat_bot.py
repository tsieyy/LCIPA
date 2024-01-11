import streamlit as st
from langchain.agents import initialize_agent, AgentType
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.callbacks.streamlit import StreamlitCallbackHandler
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableConfig
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from utils.login import make_sure_login

from chat_bot.cb_demo import llm, tools, chat


# Set up memory
msgs = StreamlitChatMessageHistory(key="langchain_messages")
if len(msgs.messages) == 0:
    msgs.add_ai_message("How can I help you?")

view_messages = st.expander("View the message contents in session state")

# Adapted from https://smith.langchain.com/hub/hwchase17/openai-tools-agent
prompt_ = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. You may not need to use tools for every query - the user may just want to chat! But when they ask you about something that happened in real life, you may need to use tools to ensure that your answers are accurate.",
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

agent = create_openai_tools_agent(chat, tools, prompt_)
agent_executor = AgentExecutor(agent=agent, tools=tools, )

chain_with_history = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: msgs,
    input_messages_key="input",
    output_messages_key="output",
    history_messages_key="history",
)

if make_sure_login():
    # Render current messages from StreamlitChatMessageHistory
    for msg in msgs.messages:
        st.chat_message(msg.type).write(msg.content)

    # If user inputs a new prompt, generate and draw a new response
    if input_msg := st.chat_input():
        st.chat_message("human").write(input_msg)
        answer_container = st.chat_message("assistant", avatar="🦜")
        st_callback = StreamlitCallbackHandler(answer_container)
        # Note: new messages are saved to history automatically by Langchain during run
        config = {"configurable": {"session_id": "any"}, "callbacks": [st_callback]}
        response = chain_with_history.invoke({"input": input_msg}, config)
        # st.chat_message("ai").write(response.content)
        # response = agent_executor.invoke({"messages": [HumanMessage(content=prompt)]})
        st.chat_message("ai").write(response['output'])

    # Draw the messages at the end, so newly generated ones show up immediately
    with view_messages:
        """
        Message History initialized with:
        ```python
        msgs = StreamlitChatMessageHistory(key="langchain_messages")
        ```

        Contents of `st.session_state.langchain_messages`:
        """
        view_messages.json(st.session_state.langchain_messages)

