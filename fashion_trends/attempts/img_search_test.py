from dotenv import load_dotenv
import os
from tavily import TavilyClient


# Load environment variables
load_dotenv()

# Check if required API keys are present
if not os.getenv("SERPER_API_KEY"):
    raise ValueError("SERPER_API_KEY environment variable is missing. Please add it to your .env file.")
if not os.getenv("ANTHROPIC_API_KEY"):
    raise ValueError("ANTHROPIC_API_KEY environment variable is missing. Please add it to your .env file.")
if not os.getenv("TAVILY_API_KEY"):
    raise ValueError("TAVILY_API_KEY environment variable is missing. Please add it to your .env file.")


tavily_client = TavilyClient()

response = tavily_client.search(query="Pistachio Green Tailored Blazer with Cream Trousers",
                                include_images=True,
                                include_image_descriptions=True)

print(response)

