from langchain_community.chat_models import ChatOpenAI
from langchain_community.tools import Tool
from langchain.agents import initialize_agent, AgentType
import json
from langchain_community.tools import DuckDuckGoSearchRun

def load_user_data():
    with open("data/user_data.json", "r", encoding="utf-8") as file:
        return json.load(file)
    
def load_product_data():
    with open("data/product_data.json", "r", encoding="utf-8") as file:
        return json.load(file)

def find_user(name: str):
    data = load_user_data()
    for user in data["users"]:
        if user["name"].lower() == name.lower():
            return user
    return "user not found in database"

def find_product(product_name: str):
    data = load_product_data()
    for product in data["products"]:
        if product["name"].lower() == product_name.lower():
            return product
    return "product not found in database"

# websearch tool 
search_tool = DuckDuckGoSearchRun()

def search_query(query: str):
    return search_tool.invoke(query)


# define tools for agent
user_search_tool = Tool(
    name="User_Database",
    func=find_user,
    description="Searches for user information in the local database. Always check here before searching the web."
)

product_search_tool = Tool(
    name="Product_Database",
    func=find_product,
    description="Searches for product information in the local database. Always check here before searching the web."
)

web_search_tool = Tool(
    name="Web_Search",
    func=search_query,
    description="Performs an internet search for a given query. Use this only if the information is not found in the local databases."
)


# Agent setup
system_prompt = """
You are an intelligent agent that should always search for information in the local database 
(user_search_tool or product_search_tool) first before using web_search_tool.
If the user asks about a product, always check Product_Database before Web_Search.
If the user asks about a user, always check User_Database before Web_Search.
"""


llm = ChatOpenAI(model_name="gpt-4o-mini")

tools = [user_search_tool, product_search_tool, web_search_tool]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# test
test_prompt_1 = "Find all information about user Alice"
test_prompt_2 = "How much does Office Chair Ergonomic cost?"
test_prompt_3 = "What are approx casualties of Japan in WW2?"

response = agent.invoke(test_prompt_3)
print(response)




