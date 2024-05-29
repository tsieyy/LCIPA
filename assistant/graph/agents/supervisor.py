from assistant.graph.utils.agent import create_supervisor
from assistant.llm_provider.openai.gpt import CHAT

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

supervisor_chain = create_supervisor(CHAT, system_prompt, members=members)
