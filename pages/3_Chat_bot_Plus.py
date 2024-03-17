
import streamlit as st
from langchain.callbacks.streamlit import StreamlitCallbackHandler
from langchain_core.messages import HumanMessage

from utils.login import make_sure_login
from chat_bot.ma_demo import graph, msgs

view_messages = st.expander("View the message contents in session state")

if make_sure_login():
    # Render current messages from StreamlitChatMessageHistory
    for msg in msgs.messages:
        st.chat_message(msg.type).write(msg.content)

    # If user inputs a new prompt, generate and draw a new response
    if input_msg := st.chat_input():
        st.chat_message("human").write(input_msg)

        config = {"configurable": {"session_id": "any"}, "recursion_limit": 100}
        # response = graph.invoke({"messages": [HumanMessage(content=input_msg)]}, config)

        stream_history = []
        with st.status("Thinking...", expanded=True) as status:
            for s in graph.stream(
                    {"messages": [HumanMessage(content=input_msg)]},
                    config,
            ):
                if "__end__" not in s:
                    st.write(str(s))
                    stream_history.append(s)
                    # print(type(s))
                    st.write("----")
            status.update(label="Complete!")

        # final output value
        final = stream_history[-2]
        value = next(iter(final.values()))
        response = value['messages'][0].content

        # memory in streamlit
        msgs.add_user_message(input_msg)
        msgs.add_ai_message(response)

        st.chat_message("ai").write(response)

    # Draw the messages at the end, so newly generated ones show up immediately
    with view_messages:
        """
        Message History initialized with:
        ```python
        msgs = StreamlitChatMessageHistory(key="langchain_messages")
        ```

        Contents of `st.session_state.ma_messages`:
        """
        view_messages.json(st.session_state.ma_messages)

