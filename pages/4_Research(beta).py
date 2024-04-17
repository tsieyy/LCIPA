import streamlit as st
from utils.login import make_sure_login
from utils.json import open_task
from chat_bot.clear_results import with_clear_container
from researcher import run_task
import asyncio

from utils.redirect import redirect_stdout_to_streamlit

# 设置页面的状态
st.set_page_config(
    page_title="Research", page_icon="🦜", layout="wide",
)

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
        task = open_task('researcher/task.json')
        task["query"] = user_input
        task["verbose"] = False
        if len(guidelines_list) == 0:
            pass
        else:
            task["guidelines"] = guidelines_list

        print(task)

        with st.status("Researching...", expanded=True) as status:
            with redirect_stdout_to_streamlit(st):
                asyncio.run(run_task(task))

            status.update(label="Complete!")
