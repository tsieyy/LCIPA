
import streamlit as st
from utils.login import make_sure_login
from utils.json import open_task
from chat_bot.clear_results import with_clear_container
from research import run_task
import asyncio

from utils.redirect import redirect_stdout_to_streamlit
from utils.file_helper import get_md_file, get_pdf_file, get_docx_file

# 设置页面的状态
st.set_page_config(
    page_title="Research", page_icon="🦜", layout="wide",
)

research_complete = False

if make_sure_login():
    with st.form(key="form"):
        user_input = st.text_input("please ask a question")
        guidelines = st.text_area(
            "You can input some guidelines, Then use \";\" to separate.",
        )
        submit_clicked = st.form_submit_button("Start Research")
    standardized_string = guidelines.replace("；", ";")
    guidelines_list = standardized_string.split(";")
    guidelines_list = [item for item in guidelines_list if item != ""]

    if with_clear_container(submit_clicked):
        task = open_task('research/task.json')
        task["query"] = user_input
        # task["verbose"] = False
        if len(guidelines_list) == 0:
            pass
        else:
            task["guidelines"] = guidelines_list

        print(task)

        with st.status("Researching...", expanded=True) as status:
            research_complete = False
            with redirect_stdout_to_streamlit(st):
                asyncio.run(run_task(task))

            status.update(label="Complete!")
            research_complete = True

    from research.agents.master import RESEARCHER_OUTPUT_PATH
    # print(RESEARCHER_OUTPUT_PATH)  # for debug

    if RESEARCHER_OUTPUT_PATH != '' and research_complete:
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
            docx = get_docx_file(RESEARCHER_OUTPUT_PATH)
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