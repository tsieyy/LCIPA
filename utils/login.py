import streamlit as st


def get_auth_status():
    try:
        status = st.session_state["authentication_status"]
    except KeyError:
        return None
    return status


def assert_login():
    s = get_auth_status()
    if s is None:
        # 还未进行登陆
        return False
    elif s is True:
        # 已登陆
        return True
    else:
        # 登陆出错
        return False
