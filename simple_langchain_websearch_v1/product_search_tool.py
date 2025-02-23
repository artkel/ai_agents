import os
import json
from langchain_community.tools import Tool

from langchain_community.document_loaders import JSONLoader
from langchain_community.agent_toolkits import JsonToolkit, create_json_agent
from langchain_community.chat_models import ChatOpenAI
from langchain_community.tools.json.tool import JsonSpec



# Load product data using JSONLoader
# product_data_loader = JSONLoader(
#     file_path="data/product_data.json",
#     jq_schema=".products[]",  
#     text_content=False
# )

# Load the raw JSON data
with open("data/product_data.json", 'r') as file:
    raw_json_data = json.load(file)

# Create JSON specification
json_spec = JsonSpec(dict_=raw_json_data, max_value_length=4000)

# Create JSON toolkit
product_search_json_toolkit = JsonToolkit(spec=json_spec)

# Initialize the LLM
llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

json_agent = create_json_agent(
    llm=llm,
    toolkit=product_search_json_toolkit,
    verbose=True
)

# # Create the product search tool from JSON toolkit
product_search_tool = Tool(
    name="Product_Database_Search",
    func=lambda q: json_agent.invoke({"input": q})["output"],
    description="Search for product-related information in the local JSON database. Always check here before searching the web."
)