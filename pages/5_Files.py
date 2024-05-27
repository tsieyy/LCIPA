import streamlit as st
from streamlit_file_browser import st_file_browser

st.header('File System')
event = st_file_browser(
    path="fs",
    # use_static_file_server=True,
    show_choose_file=True,
    show_delete_file=True,
    show_download_file=False,
    show_new_folder=True,
    show_upload_file=False,
    # static_file_server_path="http://localhost:9999/?choose=true",
)
st.write(event)



