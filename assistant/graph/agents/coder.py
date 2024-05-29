# Coder
# NOTE: THIS PERFORMS ARBITRARY CODE EXECUTION. PROCEED WITH CAUTION
import functools

from assistant.graph.utils.agent import create_agent
from assistant.llm_provider.openai.gpt import CHAT
from assistant.tools.interpreter.python import python_repl_tool
from chat_bot.graph.utils import agent_node

code_agent = create_agent(
    CHAT,
    [python_repl_tool],
    "You may generate safe python code to analyze data and generate charts using matplotlib.",
)
code_node = functools.partial(agent_node, agent=code_agent, name="Coder")
