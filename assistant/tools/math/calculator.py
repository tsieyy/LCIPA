from langchain.chains import LLMMathChain
from langchain_core.tools import Tool

from assistant.llm_provider.openai.gpt import LLM


llm_math_chain = LLMMathChain.from_llm(LLM)
calculator_tool = Tool(
    name="Calculator",
    func=llm_math_chain.run,
    description="useful for when you need to answer questions about math",
)