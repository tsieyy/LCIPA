# Researcher
import functools

from assistant.graph.utils.agent import create_agent
from assistant.graph.utils.graph import agent_node
from assistant.llm_provider.openai.gpt import CHAT
from assistant.tools.researcher.tavily_search import tavily_search_tool

research_agent = create_agent(CHAT, [tavily_search_tool], "You are a web researcher.")
research_node = functools.partial(agent_node, agent=research_agent, name="Researcher")
