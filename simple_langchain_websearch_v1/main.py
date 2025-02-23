from langchain_community.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType

# import tools
from logging_tool import logging_tool
from user_search_tool import user_search_tool
from product_search_tool import product_search_tool
from web_search_tool import web_search_tool

# import prompts
from prompts import prompts


# Agent setup
llm = ChatOpenAI(model_name="gpt-4o-mini")

tools = [user_search_tool, product_search_tool, web_search_tool, logging_tool]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Test
response = agent.invoke(prompts[8])
print(response)


