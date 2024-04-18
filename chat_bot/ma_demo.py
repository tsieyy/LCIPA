# multi-agents-demo

import functools

from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langgraph.graph import StateGraph, END

from chat_bot.graph.state import DocWritingState, AgentState
from chat_bot.graph.tool import write_document, edit_document, read_document, create_outline, python_repl
from chat_bot.lc.llm import chat as llm
from chat_bot.lc.tool import tavily_tool, python_repl_tool, calculator_tool, gmail_toolkit
from chat_bot.graph.utils import create_team_supervisor, create_supervisor, create_agent, prelude, agent_node, \
    enter_chain, get_last_message, join_graph

'''
    创建 Document Writing Team
'''
doc_writer_agent = create_agent(
    llm,
    [write_document, edit_document, read_document],
    "You are an expert writing a research document.\n"
    # The {current_files} value is populated automatically by the graph state
    "Below are files currently in your directory:\n{current_files}",
)
# Injects current directory working state before each call
context_aware_doc_writer_agent = prelude | doc_writer_agent
doc_writing_node = functools.partial(
    agent_node, agent=context_aware_doc_writer_agent, name="DocWriter"
)

note_taking_agent = create_agent(
    llm,
    [create_outline, read_document],
    "You are an expert senior researcher tasked with writing a paper outline and"
    " taking notes to craft a perfect paper.{current_files}",
)
context_aware_note_taking_agent = prelude | note_taking_agent
note_taking_node = functools.partial(
    agent_node, agent=context_aware_note_taking_agent, name="NoteTaker"
)

chart_generating_agent = create_agent(
    llm,
    [read_document, python_repl],
    "You are a data viz expert tasked with generating charts for a research project."
    "{current_files}",
)
context_aware_chart_generating_agent = prelude | chart_generating_agent
chart_generating_node = functools.partial(
    agent_node, agent=context_aware_note_taking_agent, name="ChartGenerator"
)

'''
    创建单一节点
'''

# Interlocutor
# Set up memory
msgs = StreamlitChatMessageHistory(key="ma_messages")
if len(msgs.messages) == 0:
    msgs.add_ai_message("How can I help you?")

chat_agent = create_agent(llm, [calculator_tool],
                          "You are a kind friend who can talk to people or answer their questions. Of "
                          "course, you have reliable tools that you can use to solve math, and when people "
                          "ask you questions about math, you can easily answer them.")
chat_node = functools.partial(agent_node, agent=chat_agent, name="Interlocutor")

# Researcher
research_agent = create_agent(llm, [tavily_tool], "You are a web researcher.")
research_node = functools.partial(agent_node, agent=research_agent, name="Researcher")

# Coder
# NOTE: THIS PERFORMS ARBITRARY CODE EXECUTION. PROCEED WITH CAUTION
code_agent = create_agent(
    llm,
    [python_repl_tool],
    "You may generate safe python code to analyze data and generate charts using matplotlib.",
)
code_node = functools.partial(agent_node, agent=code_agent, name="Coder")

# MailManager
mail_agent = create_agent(
    llm,
    gmail_toolkit.get_tools(),
    "You have all the tools related to mail and can send or read messages through Gmail."
)
mail_node = functools.partial(agent_node, agent=mail_agent, name='MailManager')


'''
    创建 Supervisor
'''
members = ["Researcher", "Coder", "Interlocutor", "MailManager", "DocWriter", "NoteTaker", "ChartGenerator"]
system_prompt = (
    "You are a supervisor tasked with managing a conversation between the"
    " following workers:  {members}. Given the following user request,"
    " respond with the worker to act next. Each worker will perform a"
    " task and respond with their results and status. When finished,"
    " respond with FINISH. In particular, user may only want to have"
    " a simple conversation and not need to complete certain tasks, "
    "in this case just use Interlocutor, and then respond with FINISH."
)

supervisor_chain = create_supervisor(llm, system_prompt, members=members)


workflow = StateGraph(AgentState)
workflow.add_node("Interlocutor", chat_node)
workflow.add_node("Researcher", research_node)
workflow.add_node("Coder", code_node)
workflow.add_node("MailManager", mail_node)
workflow.add_node("supervisor", supervisor_chain)
workflow.add_node("DocWriter", doc_writing_node)
workflow.add_node("NoteTaker", note_taking_node)
workflow.add_node("ChartGenerator", chart_generating_node)

for member in members:
    # We want our workers to ALWAYS "report back" to the supervisor when done
    workflow.add_edge(member, "supervisor")
# The supervisor populates the "next" field in the graph state
# which routes to a node or finishes
conditional_map = {k: k for k in members}
conditional_map["FINISH"] = END
workflow.add_conditional_edges("supervisor", lambda x: x["next"], conditional_map)
# Finally, add entrypoint
workflow.set_entry_point("supervisor")

graph = workflow.compile()
