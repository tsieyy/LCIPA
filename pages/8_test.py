import os

import streamlit as st

from utils.file_helper import get_md_file, get_pdf_file, get_docx_file


RESEARCHER_OUTPUT_PATH = 'fs/research/run_1716875600_湖北工业大学在中国的发展如何？'


col1, col2, col3 = st.columns(3)
with col1:
    with open(get_pdf_file(RESEARCHER_OUTPUT_PATH), "rb") as file:
        btn1 = st.download_button(
            label="Download PDF",
            data=file,
            file_name="research.pdf",
            mime="application/pdf"
        )

with col2:
    with open(get_md_file(RESEARCHER_OUTPUT_PATH), "rb") as file:
        btn2 = st.download_button(
            label="Download Markdown",
            data=file,
            file_name="research.md",
            mime="text/x-markdown"
        )

with col3:
    with open(get_docx_file(RESEARCHER_OUTPUT_PATH), "rb") as file:
        btn3 = st.download_button(
            label="Download Docx",
            data=file,
            file_name="research.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )