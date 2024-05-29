import streamlit as st
from langchain.callbacks.streamlit import StreamlitCallbackHandler

from utils.login import make_sure_login
from chat_bot.cb_demo import msgs, chain_with_history

view_messages = st.expander("View the message contents in session state")

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

