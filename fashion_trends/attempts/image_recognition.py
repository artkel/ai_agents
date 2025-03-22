from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
SPIDER_API_KEY = os.getenv("SPIDER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "describe the image using only max 10 words."},
            {
                "type": "image_url",
                "image_url": {
                    "url": "https://heuritech.com/wp-content/uploads/2024/10/Screenshot-2024-10-21-at-14.27.25.png.webp",
                },
            },
        ],
    }],
)

print(response.choices[0].message.content)