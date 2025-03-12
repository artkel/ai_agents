import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Spider API key from environment variables
SPIDER_API_KEY = os.getenv("SPIDER_API_KEY")

if not SPIDER_API_KEY:
    raise ValueError("SPIDER_API_KEY environment variable is missing. Please add it to your .env file.")

headers = {
    'Authorization': f'Bearer {SPIDER_API_KEY}',
    'Content-Type': 'application/json'}

json_data = {"limit": 1,
             "readability": True,
             "url": "https://www.harpersbazaar.com/fashion/trends/a62302060/spring-2025-fashion-trends/",
             "return_format": "markdown"}

response = requests.post('https://api.spider.cloud/crawl',
                    headers=headers,
                    json=json_data)

print(response.json()[0]['url'])
print("##########################")

full_content = response.json()[0]['content']
trend_name = "## Asymmetrical Skirts"
trend_index = full_content.find(trend_name)

if trend_index >= 0:
    # Extract exactly 1000 characters after the trend name
    chars_after_trend = 1000

    # Include the trend name itself, some context before it, and chars_after_trend characters after it
    context_before = 100  # Characters before the trend name for context
    section_start = max(0, trend_index - context_before)
    section_end = 10

    trend_section = full_content[section_start:section_end]

    print(trend_section)
else:
    print(f"Error: Could not find trend '{trend_name}' in the article. Please check the spelling.")


print(response.json()[0]['content'])
