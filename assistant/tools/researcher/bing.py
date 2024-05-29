# bing search tool

from langchain_community.tools import BingSearchRun
from langchain_community.utilities import BingSearchAPIWrapper

bing_search_api = BingSearchAPIWrapper(k=3)
bing_search = BingSearchRun(api_wrapper=bing_search_api)
bing_search.name = 'BingSearch'
bing_search.description = 'This is Bing search tool. Useful for searching some real time info, such as news.'
