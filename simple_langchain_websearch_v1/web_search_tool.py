from langchain_community.tools import Tool
from langchain_community.tools import DuckDuckGoSearchRun


# websearch tool 
search_tool = DuckDuckGoSearchRun()

def search_query(query: str):
    return search_tool.invoke(query)

web_search_tool = Tool(
    name="Web_Search",
    func=search_query,
    description="Performs an internet search for a given query. Use this only if the information is not found in the local databases."
)