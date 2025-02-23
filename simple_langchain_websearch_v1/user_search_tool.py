import os
import json
from langchain_community.tools import Tool

from langchain_community.document_loaders import JSONLoader
from langchain_community.agent_toolkits import JsonToolkit, create_json_agent
from langchain_community.chat_models import ChatOpenAI
from langchain_community.tools.json.tool import JsonSpec



# Load user data using JSONLoader
# user_data_loader = JSONLoader(
#     file_path="data/user_data.json",
#     jq_schema=".users[]",  
#     text_content=False
# )

# Load the raw JSON data
with open("data/user_data.json", 'r') as file:
    raw_json_data = json.load(file)

# Create JSON specification
json_spec = JsonSpec(dict_=raw_json_data, max_value_length=4000)

# Create JSON toolkit
user_search_json_toolkit = JsonToolkit(spec=json_spec)

# Initialize the LLM
llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

json_agent = create_json_agent(
    llm=llm,
    toolkit=user_search_json_toolkit,
    verbose=True
)

# # Create the user search tool from JSON toolkit
user_search_tool = Tool(
    name="User_Database_Search",
    func=lambda q: json_agent.invoke({"input": q})["output"],
    description="Search for user-related information in the local JSON database. Always check here before searching the web."
)



# # Function to query the JSON agent
# def query_json_data(query: str) -> str:
#     try:
#         response = json_agent.invoke({"input": query})
#         return response["output"]
#     except Exception as e:
#         return f"Error processing query: {str(e)}"

# # Example usage
# if __name__ == "__main__":

#     # Example queries
#     queries = [
#         "How many users are in the database?",
#         "What are the names of all users?",
#         "Find users who are older than 30"
#     ]
    
#     for query in queries:
#         print(f"\nQuery: {query}")
#         result = query_json_data(query)
#         print(f"Response: {result}")



# # to read data from json files
# def load_user_data():
#     with open("data/user_data.json", "r", encoding="utf-8") as file:
#         return json.load(file)
    
# def load_product_data():
#     with open("data/product_data.json", "r", encoding="utf-8") as file:
#         return json.load(file)


# # User search function
# def find_user(name: str):
#     data = load_user_data()
#     for user in data["users"]:
#         if user["name"].lower() == name.lower():
#             return user
#     return "User not found"

# # Product search function
# def find_product(product_name: str):
#     data = load_product_data()
#     for product in data["products"]:
#         if product["name"].lower() == product_name.lower():
#             return product
#     return "Product not found"




# # define tools for agent
# user_search_tool = Tool(
#     name="User_Database",
#     func=find_user,
#     description="Searches for user information in the local database. Always check here before searching the web."
# )

# product_search_tool = Tool(
#     name="Product_Database",
#     func=find_product,
#     description="Searches for product information in the local database. Always check here before searching the web."
# )



