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
test_prompt_1 = "Find all information about user Alice. Use logging tool to save logs!"
test_prompt_2 = "How much does Office Chair Ergonomic cost? Use logging tool to save logs!"
test_prompt_3 = "What are approx casualties of Japan in WW2? Use logging tool to save logs!"
test_prompt_4 = "How old Bob is? And where does he live? Use logging tool to save logs!"
test_prompt_5 = "Which product is the most expensive? Use logging tool to save logs!"
test_prompt_6 = "Who is the oldest user from hamburg in our database? Use logging tool to save logs!"
test_prompt_7 = "Give me all products that are 200 or cheaper. Use logging tool to save logs!"


response = agent.invoke(test_prompt_6)
print(response)


