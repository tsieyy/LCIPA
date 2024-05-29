# MailManager
import functools

from assistant.graph.utils.agent import create_agent
from assistant.graph.utils.graph import agent_node
from assistant.llm_provider.openai.gpt import CHAT
from assistant.tools.mails.gmail import gmail_toolkit

mail_agent = create_agent(
    CHAT,
    gmail_toolkit.get_tools(),
    "You have all the tools related to mail and can send or read messages through Gmail."
)
mail_node = functools.partial(agent_node, agent=mail_agent, name='MailManager')