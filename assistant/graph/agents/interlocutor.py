# Interlocutor
import functools

from assistant.graph.utils.agent import create_agent
from assistant.graph.utils.graph import agent_node
from assistant.llm_provider.openai.gpt import CHAT
from assistant.tools.math.calculator import calculator_tool

chat_agent = create_agent(CHAT, [calculator_tool],
                          "You are a kind friend who can talk to people or answer their questions. Of "
                          "course, you have reliable tools that you can use to solve math, and when people "
                          "ask you questions about math, you can easily answer them.")
chat_node = functools.partial(agent_node, agent=chat_agent, name="Interlocutor")