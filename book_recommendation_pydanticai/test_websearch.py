from pydantic_ai import Agent
from pydantic_ai.common_tools.duckduckgo import duckduckgo_search_tool
from dotenv import load_dotenv
from pydantic_ai.models.openai import OpenAIModel
#from typing_extensions import TypedDict
#from pydantic_ai.models.anthropic import AnthropicModel
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OpenAI API key is required. Please set the OpenAI_API_KEY environment variable.")

# Create an OpenAI with the API key
model = OpenAIModel(
    "gpt-3.5-turbo-0125",
    api_key=api_key
)

# Extraction agent to process search results into structured book information
agent = Agent(
    model=model,
    tools=[duckduckgo_search_tool()],
    system_prompt=(
        'You are a search assistant that ALWAYS uses the DuckDuckGo search tool to find information. '
        'For any user query, your first step must be to use the search tool with appropriate search terms. '
        'Never try to answer directly from your knowledge - always search first, then provide a response based on '
        'the search results. This is critical even for questions you think you know the answer to.'
    )
)

# Function to help ensure we search properly
def search_query(user_query):
    # Prepare a prompt that explicitly tells the agent to use the search tool
    full_prompt = f"Search for information about: {user_query}"
    return agent.run_sync(full_prompt)

# Use the function with your query
result = search_query('Last FC Barcelona fixture result on March 2nd 2025')
messages = result.all_messages()
print(messages)