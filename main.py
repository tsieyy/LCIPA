import streamlit as st
import streamlit_authenticator as stauth

import yaml
from yaml.loader import SafeLoader

from utils.login import assert_login


# 设置页面的状态
st.set_page_config(
    page_title="Chat-Bot", page_icon="🦜", layout="wide", initial_sidebar_state="collapsed"
)


with open('config/passwd.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)


@st.experimental_dialog("Login")
def _login():
    # 启动登陆功能
    authenticator.login()


@st.experimental_dialog("Register")
def _register():
    try:
        email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(
            pre_authorization=False)
        if email_of_registered_user:
            st.success('User registered successfully')
    except Exception as e:
        st.error(e)


if not assert_login():
    col1, col2 = st.columns(2)
    with col1:
        st.header('Login')
        st.write('click this button below to login.')
        if st.button('Login', use_container_width=True):
            _login()

    with col2:
        st.header('Register')
        st.write('if you don\'t have a account, you can register.')
        if st.button('Register', use_container_width=True):
            _register()

else:
    st.write('login success')

