# serp api for Google search

from langchain.utilities import SerpAPIWrapper
from langchain_core.tools import Tool

serp_api = SerpAPIWrapper()
serp_search_tool = Tool(
    name="GoogleSearch",
    func=serp_api.run,
    description="This is Google search tool. Useful for searching some real time info, such as news.",
)