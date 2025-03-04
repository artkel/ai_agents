from smolagents import CodeAgent, HfApiModel, Tool, DuckDuckGoSearchTool
import os
from dotenv import load_dotenv
from smolagents import LiteLLMModel
from sympy.physics.units import temperature

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
hf_token = os.getenv("HF_TOKEN")


# Initialize the search tool
search_tool = DuckDuckGoSearchTool()

# Initialize the model with Claude 3 Haiku
# model = HfApiModel()

# Instantiate Anthropic model
model = LiteLLMModel(
    model_id = "anthropic/claude-3-5-sonnet-20241022",
    temperature=0.2,
    api_key=anthropic_api_key,
    max_tokens=500
)


# Create the agent with the model and search tool
agent = CodeAgent(
    model=model,
    tools=[search_tool],
    #verbose=True
)

prompt = """Search for the latest fashion trends for women in 2025. For each of the top three trends, provide:

1) SUMMARY: A brief, concise description of the trend (2-3 sentences maximum)
2) OUTFIT IDEAS: Three specific outfit combinations that incorporate this trend
3) SHOPPING IDEAS: Where to find these items (mention both specific retailers and types of stores)

Format your response with clear headings for each trend and numbered lists for outfit ideas. Keep the information concise and actionable.
Translate your response in Russian language."""

response = agent.run(
    prompt
)

print(response)