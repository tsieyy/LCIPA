import functools

from langgraph.graph import StateGraph, END

from langchain_community.chat_message_histories import StreamlitChatMessageHistory

from assistant.graph.agents.coder import code_node
from assistant.graph.agents.doc_handler import doc_writing_node, note_taking_node, chart_generating_node
from assistant.graph.agents.interlocutor import chat_node
from assistant.graph.agents.mailman import mail_node
from assistant.graph.agents.researcher import research_node
from assistant.graph.agents.supervisor import supervisor_chain, members
from assistant.graph.state.agent.agent_state import AgentState


# Set up memory
msgs = StreamlitChatMessageHistory(key="ma_messages")
if len(msgs.messages) == 0:
    msgs.add_ai_message("How can I help you?")

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
