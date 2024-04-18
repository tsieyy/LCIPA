import streamlit as st
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu

import yaml
from yaml.loader import SafeLoader

from utils.login import assert_login
# from utils.welcome import CCBOT


# 设置页面的状态
st.set_page_config(
    page_title="Chat-Bot", page_icon="🦜", layout="wide", initial_sidebar_state="collapsed"
)

# TODO: design the menu
# with st.sidebar:
#     selected = option_menu("Main Menu", ["Home", 'Settings'],
#         icons=['house', 'gear'], menu_icon="cast", default_index=1)
#


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
    # TODO： 需要加上一些欢迎语句 到时候再写把
    st.success('Login Success!', icon="✅")
    with open('README.md', 'r') as file:
        # 读取文件内容
        content = file.read()
    st.markdown(content)
