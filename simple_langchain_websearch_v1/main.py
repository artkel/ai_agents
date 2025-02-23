from langchain_community.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType

# import tools
from logging_tool import logging_tool
from user_search_tool import user_search_tool
from product_search_tool import product_search_tool
from web_search_tool import web_search_tool


# Agent setup
llm = ChatOpenAI(model_name="gpt-4o-mini")

tools = [user_search_tool, product_search_tool, web_search_tool, logging_tool]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# test
test_prompt_1 = "Find all available information about the user named Alice. Use the logging tool to save logs."
test_prompt_2 = "What is the price of the Office Chair Ergonomic? Use the logging tool to save logs."
test_prompt_3 = "What were the approximate casualties in Japan during World War II? Use the logging tool to save logs."
test_prompt_4 = "How old is Bob and where does he live? Use the logging tool to save logs."
test_prompt_5 = "Which product is the most expensive in our database? Use the logging tool to save logs."
test_prompt_6 = "Who is the oldest user from Hamburg in our database? Use the logging tool to save logs."
test_prompt_7 = "List all products that cost $200 or less. Use the logging tool to save logs."
test_prompt_8 = "Who was the President of the United States during the reign of Emperor Alexander I of Russia (early 19th century)? Use the logging tool to save logs."


response = agent.invoke(test_prompt_8)
print(response)


