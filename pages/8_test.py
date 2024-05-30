import os

import streamlit as st

from utils.file_helper import get_md_file, get_pdf_file, get_docx_file

RESEARCHER_OUTPUT_PATH = 'fs/research/run_1716875600_湖北工业大学在中国的发展如何？'

col1, col2, col3 = st.columns(3)
with col1:
    st.write("PDF")
    pdf = get_pdf_file(RESEARCHER_OUTPUT_PATH)
    if pdf is not None:
        with open(pdf, "rb") as file:
            btn1 = st.download_button(
                label="Download PDF",
                data=file,
                file_name="research.pdf",
                mime="application/pdf"
            )
    else:
        st.warning("Oops, maybe the file wasn't generated...", icon='⚠️')

with col2:
    st.write("Markdown")
    md = get_md_file(RESEARCHER_OUTPUT_PATH)
    if md is not None:
        with open(md, "rb") as file:
            btn2 = st.download_button(
                label="Download Markdown",
                data=file,
                file_name="research.md",
                mime="text/x-markdown"
            )
    else:
        st.warning("Oops, maybe the file wasn't generated...", icon='⚠️')

with col3:
    st.write("Docx")
    # docx = get_docx_file(RESEARCHER_OUTPUT_PATH)
    docx = None
    if docx is not None:
        with open(md, "rb") as file:
            btn3 = st.download_button(
                label="Download Docx",
                data=file,
                file_name="research.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
    else:
        st.warning("Oops, maybe the file wasn't generated...", icon='⚠️')