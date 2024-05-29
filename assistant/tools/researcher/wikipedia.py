# wikipedia tool.

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

wiki_api = WikipediaAPIWrapper(top_k_result=1, doc_content_chars_max=100)
wiki_search_tool = WikipediaQueryRun(api_wrapper=wiki_api)
wiki_search_tool.name = 'Wikipedia'
wiki_search_tool.description = (
    'A wrapper around Wikipedia. Useful for when you need to answer general question about '
    'definition and the description of people, place, facts, history etc.'
)
