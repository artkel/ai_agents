import os
from dotenv import load_dotenv
from scrapfly import ScrapflyClient, ScrapeConfig, ExtractionConfig, ScrapeApiResponse

# Load environment variables
load_dotenv()

# Get Scrapfly API key
SCRAPFLY_API_KEY = os.getenv("SCRAPFLY_API_KEY")

if not SCRAPFLY_API_KEY:
    raise ValueError("SCRAPFLY_API_KEY environment variable is missing")

# Initialize Scrapfly client
client = ScrapflyClient(key=SCRAPFLY_API_KEY)

# URL of the fashion trend article
url = "https://www.glamour.com/story/2025-fashion-trends"

# api_response:ScrapeApiResponse = scrapfly.scrape(scrape_config=ScrapeConfig(url=url))
#
# print(api_response.scrape_result)





# First, scrape the webpage content
scrape_result = client.scrape(ScrapeConfig(
    url=url,
    format="markdown",
    render_js=True,  # Enable JavaScript rendering
    asp=True         # Anti-scraping protection bypass
))

# Extract the trend information using a specific extraction prompt
extraction_result = client.extract(ExtractionConfig(
    body=scrape_result.content,
    content_type="text/html",
    extraction_prompt="""
    Extract fashion trend information from this webpage.
    For the first trend only, return:
    - trend_name: The name/title of the trend
    - trend_description: A brief description of the trend
    - image_url: URL of an image showing the trend
    - image_description: A brief description of what the image shows
    - source_url: The URL of this webpage
    """
))

# Print the extracted data
print("Extracted Trend Data:")
print(extraction_result.result)