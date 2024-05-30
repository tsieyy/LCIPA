import streamlit as st
from langchain.callbacks.streamlit import StreamlitCallbackHandler
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.runnables import RunnableConfig

from utils.login import make_sure_login

from chat_bot.clear_results import with_clear_container
from chat_bot import cb_demo
from chat_bot.cb_demo import llm, mrkl
from chat_bot.cb_demo import configure_retriever, PrintRetrievalHandler, StreamHandler
from chat_bot.cb_demo import create_agent_db_from_url



# 设置页面的状态
st.set_page_config(
    page_title="Chat-Bot", page_icon="🦜", layout="wide",
)

if make_sure_login():
    # 侧边栏选择项
    radio_opt = ["None", "Use local database", "Connect to your SQL database"]
    selected_opt = st.sidebar.radio(label="Choose suitable option", options=radio_opt)
    if radio_opt.index(selected_opt) == 2:
        st.sidebar.warning(cb_demo.INJECTION_WARNING, icon="⚠️")
        db_uri = st.sidebar.text_input(
            label="Database URI", placeholder="mysql://user:pass@hostname:port/db"
        )
    else:
        db_uri = cb_demo.LOCALDB

    agent_db = create_agent_db_from_url(db_uri)

    # 文件上传项
    uploaded_files = st.sidebar.file_uploader(
        label="Upload PDF files", type=["pdf"], accept_multiple_files=True
    )
    
    # 主要业务逻辑
    if uploaded_files:
        retriever = configure_retriever(uploaded_files)

        # Setup memory for contextual conversation
        msgs = StreamlitChatMessageHistory()
        memory = ConversationBufferMemory(memory_key="chat_history", chat_memory=msgs, return_messages=True)

        # Setup QA chain
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=llm, retriever=retriever, memory=memory, verbose=True
        )

        if len(msgs.messages) == 0 or st.sidebar.button("Clear message history"):
            msgs.clear()
            msgs.add_ai_message("How can I help you?")

        avatars = {"human": "user", "ai": "assistant"}
        for msg in msgs.messages:
            st.chat_message(avatars[msg.type]).write(msg.content)

        if user_query := st.chat_input(placeholder="Ask me anything!"):
            st.chat_message("user").write(user_query)

            with st.chat_message("assistant"):
                retrieval_handler = PrintRetrievalHandler(st.container())
                stream_handler = StreamHandler(st.empty())
                response = qa_chain.run(user_query, callbacks=[retrieval_handler, stream_handler])

    elif radio_opt.index(selected_opt) != 0:
        if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
            st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        user_query = st.chat_input(placeholder="Ask me anything!")

        if user_query:
            st.session_state.messages.append({"role": "user", "content": user_query})
            st.chat_message("user").write(user_query)

            with st.chat_message("assistant"):
                st_cb = StreamlitCallbackHandler(st.container())
                response = agent_db.run(user_query, callbacks=[st_cb])
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.write(response)

    else:
        with st.form(key="form"):
            user_input = st.text_input("please ask a question")
            submit_clicked = st.form_submit_button("Submit Question")

        output_container = st.empty()
        if with_clear_container(submit_clicked):
            output_container = output_container.container()
            output_container.chat_message("user").write(user_input)

            answer_container = output_container.chat_message("assistant", avatar="🦜")
            st_callback = StreamlitCallbackHandler(answer_container)
            cfg = RunnableConfig()
            cfg["callbacks"] = [st_callback]

            # If we've saved this question, play it back instead of actually running LangChain
            # (so that we don't exhaust our API calls unnecessarily)

            answer = mrkl.invoke({"input": user_input}, cfg)

            answer_container.write(answer["output"])
