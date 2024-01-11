

#制备Bing搜索
from langchain_community.tools import BingSearchRun
from langchain_community.utilities import BingSearchAPIWrapper
search_api = BingSearchAPIWrapper(k=1)
searchtool = BingSearchRun(api_wrapper=search_api)
searchtool.name = 'BingSearch'
searchtool.description ='This is Bing search tool. Useful for searching some real time info, such as news.'


#制备维基百科工具.定义name，description，JSON schema，the function to call, result return to user directly or not
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
api_wrapper = WikipediaAPIWrapper(top_k_result=1, doc_content_chars_max=100)
wikitool = WikipediaQueryRun(api_wrapper=api_wrapper)
wikitool.name = 'Wikipedia'
wikitool.description ='A wrapper around Wikipedia. Useful for when you need to answer general question about definition and the description of people, place, facrts, history etc.'


# 制备Google搜索
from langchain.utilities import SerpAPIWrapper
# from langchain.agents import load_tools
serp_api = SerpAPIWrapper()
# google_tool = GoogleSearchRun(api_wrapper=serp_api)
# google_tool.name = 'GoogleSearch'
# google_tool.description = 'This is Google search tool. Useful for searching some real time info, such as news.'



from langchain.agents import AgentExecutor, Tool, create_react_agent
from langchain.chains import LLMMathChain
from .llm import llm

llm_math_chain = LLMMathChain.from_llm(llm)

tools = [
    Tool(
        name="Calculator",
        func=llm_math_chain.run,
        description="useful for when you need to answer questions about math",
    ),
    Tool(
        name="Google Search",
        func=serp_api.run,
        description="This is Google search tool. Useful for searching some real time info, such as news.",
    ),
    searchtool,
    wikitool,
]