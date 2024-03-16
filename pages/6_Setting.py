import streamlit as st

from main import authenticator
from utils.login import make_sure_login


# 设置页面的状态
st.set_page_config(
    page_title="Chat-Bot", page_icon="🦜", layout="wide", initial_sidebar_state="collapsed"
)


@st.experimental_dialog("Logout")
def _logout():
    st.warning("Are you sure to logout?")
    if st.session_state["authentication_status"]:
        authenticator.logout()
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')


@st.experimental_dialog("Reset")
def _reset():
    if st.session_state["authentication_status"]:
        try:
            if authenticator.reset_password(st.session_state["username"]):
                st.success('Password modified successfully')
        except Exception as e:
            st.error(e)


if make_sure_login():
    # 登陆成功后
    col1, col2 = st.columns(2)

    with col1:
        st.header("Logout")
        if st.button('Logout', use_container_width=True):
            _logout()

    with col2:
        st.header("Reset")
        if st.button("Reset", use_container_width=True):
            _reset()

    # file uploader for RAG
    st.write("you can choose to upload files to open RAG.")
    uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)
    if 'up_files' not in st.session_state:
        st.session_state['up_files'] = uploaded_files




