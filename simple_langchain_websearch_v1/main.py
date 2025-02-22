from langchain_community.chat_models import ChatOpenAI
from langchain_community.tools import Tool
from langchain.agents import initialize_agent, AgentType
import json
import os
from langchain_community.tools import DuckDuckGoSearchRun
import datetime

# to read data from json files
def load_user_data():
    with open("data/user_data.json", "r", encoding="utf-8") as file:
        return json.load(file)
    
def load_product_data():
    with open("data/product_data.json", "r", encoding="utf-8") as file:
        return json.load(file)
    
# Logging function
log_path = os.path.join("data", "log.txt")

# Logging function

def log_interaction(query, tool_used, response):
    if not os.path.exists(log_path):
        open(log_path, "w")

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now()} | Query: {query} | Response: {response}\n")

    return "log saved"


# User search function
def find_user(name: str):
    data = load_user_data()
    for user in data["users"]:
        if user["name"].lower() == name.lower():
            response = user
            log_interaction(name, "User_Database", response)
            return response
    response = "User not found"
    log_interaction(name, "User_Database", response)
    return response

# Product search function
def find_product(product_name: str):
    data = load_product_data()
    for product in data["products"]:
        if product["name"].lower() == product_name.lower():
            response = product
            log_interaction(product_name, "Product_Database", response)
            return response
    response = "Product not found"
    log_interaction(product_name, "Product_Database", response)
    return response

# websearch tool 
search_tool = DuckDuckGoSearchRun()

def search_query(query: str):
    response = search_tool.invoke(query)
    log_interaction(query, "Web_Search", response)
    return response


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
test_prompt_4 = "How old Bob is? And where does he live?"

response = agent.invoke(test_prompt_3)
print(response)




