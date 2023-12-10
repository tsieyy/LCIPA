import streamlit as st

from main import authenticator
from utils.login import assert_login


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


if not assert_login():
    st.info('You need login first! Please switch to main page to login.', icon="ℹ️")
else:
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



