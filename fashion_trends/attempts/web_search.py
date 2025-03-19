# Warning control
import warnings, os, json, sqlite3, datetime
warnings.filterwarnings('ignore')
from typing import List, Optional
from pydantic import BaseModel, Field
from crewai import Agent, Task, Crew
from crewai.tools import BaseTool
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# Set them explicitly in os.environ to ensure they're available to the libraries
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["SERPER_API_KEY"] = SERPER_API_KEY

# Check if keys were loaded properly
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env file")
if not SERPER_API_KEY:
    raise ValueError("SERPER_API_KEY not found in .env file")

# Define Pydantic models for structured output
class FashionTrend(BaseModel):
    trend_name: str = Field(description="The exact name of the fashion trend as mentioned in the article")
    source_url: str = Field(description="URL of the article where the trend was found")

class FashionTrends(BaseModel):
    trends: List[FashionTrend] = Field(description="List of three verified fashion trends from different sources")

# Database functions remain the same
def setup_database():
    """Create the trends table if it doesn't exist."""
    conn = sqlite3.connect('fashion_trends.db')
    cursor = conn.cursor()

    # Create the trends table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS trends (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trend_name TEXT UNIQUE NOT NULL,
        source_url TEXT NOT NULL,
        discovered_date TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()


def trend_exists(trend_name):
    """Check if a trend already exists in the database."""
    conn = sqlite3.connect('fashion_trends.db')
    cursor = conn.cursor()

    # Case-insensitive search
    cursor.execute('SELECT 1 FROM trends WHERE LOWER(trend_name) = LOWER(?)', (trend_name,))
    result = cursor.fetchone() is not None

    conn.close()
    return result


def add_trend(trend_name, source_url):
    """Add a new trend to the database."""
    import datetime

    conn = sqlite3.connect('fashion_trends.db')
    cursor = conn.cursor()

    try:
        cursor.execute(
            'INSERT INTO trends (trend_name, source_url, discovered_date) VALUES (?, ?, ?)',
            (trend_name, source_url, datetime.datetime.now().isoformat())
        )
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        # This happens if we try to insert a duplicate trend
        success = False
    finally:
        conn.close()

    return success


def get_all_trends():
    """Retrieve all trends from the database."""
    conn = sqlite3.connect('fashion_trends.db')
    conn.row_factory = sqlite3.Row  # This allows access to columns by name
    cursor = conn.cursor()

    cursor.execute('SELECT trend_name, source_url, discovered_date FROM trends')
    trends = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return trends


def get_used_urls():
    """Retrieve all source URLs from the database."""
    conn = sqlite3.connect('fashion_trends.db')
    cursor = conn.cursor()

    cursor.execute('SELECT source_url FROM trends')
    urls = [row[0] for row in cursor.fetchall()]

    conn.close()
    return urls


# Simplified BlocklistTool that reads from config/blocked_urls.json
class BlocklistInput(BaseModel):
    """Input schema for BlocklistTool."""
    action: str = Field(..., description="Action to perform: 'check' or 'list'")
    url: Optional[str] = Field(None, description="URL to check against the blocklist")

# TrendDatabaseTool definition
class TrendDatabaseInput(BaseModel):
    """Input schema for TrendDatabaseTool."""
    action: str = Field(..., description="Action to perform: 'check', 'add', or 'list'")
    trend_name: Optional[str] = Field(None, description="Name of the trend to check or add")
    source_url: Optional[str] = Field(None, description="URL source for the trend")

# create tools
class BlocklistTool(BaseTool):
    name: str = "URL Blocklist Tool"
    description: str = """
    Tool to check if a URL is on the blocklist.
    Use it to:
    - Check if a URL is blocked ('check' action)
    - List all blocked URLs ('list' action)
    """
    args_schema: type[BaseModel] = BlocklistInput

    def _get_blocked_urls(self):
        """Read the blocked URLs from the JSON file."""
        blocklist_path = 'config/blocked_urls.json'
        try:
            if os.path.exists(blocklist_path):
                with open(blocklist_path, 'r') as f:
                    return json.load(f)
            return []
        except json.JSONDecodeError:
            # Handle case where file exists but is empty or malformed
            return []

    def _run(self, action: str, url: Optional[str] = None) -> str:
        """Execute the tool based on the action."""
        blocked_urls = self._get_blocked_urls()

        if action == 'check':
            if not url:
                return "Error: url is required for 'check' action"

            # Check if the URL or any part of it is in the blocklist
            for blocked_url in blocked_urls:
                if blocked_url in url:
                    return f"The URL '{url}' is blocked because it contains '{blocked_url}'."

            return f"The URL '{url}' is not blocked."

        elif action == 'list':
            if not blocked_urls:
                return "No URLs are currently blocked."

            result = "Currently blocked URLs:\n"
            for i, blocked_url in enumerate(blocked_urls, 1):
                result += f"{i}. {blocked_url}\n"
            return result

        else:
            return f"Error: Unknown action '{action}'. Use 'check' or 'list'."

class TrendDatabaseTool(BaseTool):
    name: str = "Trend Database Tool"
    description: str = """
    Tool to interact with the fashion trends database.
    Use it to:
    - Check if a trend already exists ('check' action)
    - Add a new trend to the database ('add' action)
    - List all existing trends ('list' action)
    """
    args_schema: type[BaseModel] = TrendDatabaseInput

    def __init__(self):
        super().__init__()
        # Ensure database is set up when tool is created
        setup_database()

    def _run(self, action: str, trend_name: Optional[str] = None, source_url: Optional[str] = None) -> str:
        """Execute the tool based on the action."""
        if action == 'check':
            if not trend_name:
                return "Error: trend_name is required for 'check' action"

            exists = trend_exists(trend_name)
            return f"The trend '{trend_name}' {'already exists' if exists else 'does not exist'} in the database."

        elif action == 'add':
            if not trend_name or not source_url:
                return "Error: both trend_name and source_url are required for 'add' action"

            success = add_trend(trend_name, source_url)
            if success:
                return f"Successfully added trend '{trend_name}' to the database."
            else:
                return f"Failed to add trend '{trend_name}'. It may already exist."

        elif action == 'list':
            trends = get_all_trends()
            if not trends:
                return "No trends found in the database."

            result = "Existing fashion trends:\n"
            for i, trend in enumerate(trends, 1):
                result += f"{i}. {trend['trend_name']} (Source: {trend['source_url']})\n"
            return result

        else:
            return f"Error: Unknown action '{action}'. Use 'check', 'add', or 'list'."


# Initialize the tools
search_tool = SerperDevTool(n_results=20)
scrape_tool = ScrapeWebsiteTool(text_content=True)
db_tool = TrendDatabaseTool()
blocklist_tool = BlocklistTool()

# Create a fashion researcher agent with all tools
fashion_researcher = Agent(
    role="Fashion Trend Researcher and Verifier",
    goal="Find and verify new women's fashion trends for 2025 that haven't been discovered before",
    backstory="""You are an expert fashion researcher who stays on top of upcoming trends. 
    Your specialty is identifying emerging women's fashion trends from reliable sources.
    You are also meticulous about verifying information and ensuring you don't duplicate trends.""",
    tools=[search_tool, scrape_tool, db_tool, blocklist_tool],
    verbose=True,
    llm="openai/gpt-4o-mini-2024-07-18"
)

# Create an enhanced search and verification task with database checks and blocklist
fashion_task = Task(
    description="""
    Your task is to find new, verified women's fashion trends for 2025 that aren't already in our database:

    1. First, use the database tool with 'list' action to see what trends we already know about

    2. Check the blocklist using the 'list' action to see what URLs are prohibited

    3. Then, search for these exact keywords to find potential new trends:
       - "Women fashion trends 2025"
       - "Women's clothing trends 2025"
       - "New women's style 2025"

    4. For each potential trend you find:
       - Check if its source URL is on the blocklist using the 'check' action
       - If the URL is blocked, reject it immediately and continue searching
       - Check if the trend already exists in our database using the 'check' action
       - If it does exist, skip it and look for another trend
       - Use the scraping tool to verify that the trend actually appears in the article
       - If verified, add it with exact same name to your findings

    5. Once you verify a trend that's not in our database, use the 'add' action to add it

    6. Continue until you have found THREE different new verified fashion trends

    CRITICAL REQUIREMENTS:
    - You MUST check each URL against the blocklist before accepting it
    - NEVER use a URL that appears on the blocklist
    - Try to use different URLs for the three trends when possible
    - A trend is only considered verified if the exact trend name appears in the article content
    - You must prioritize trends that are explicitly mentioned as 2025 trends
    - The trend must NOT already exist in our database (case-insensitive check)
    """,
    expected_output="A JSON object with three new verified fashion trends, each containing the trend name and source URL",
    agent=fashion_researcher,
    output_pydantic=FashionTrends
)

# Ensure database is set up
setup_database()


# Create and run the crew
crew = Crew(
    agents=[fashion_researcher],
    tasks=[fashion_task],
    verbose=True
)

# Execute the crew
result = crew.kickoff()

# Print the structured result
print("\n===== NEW VERIFIED FASHION TRENDS FOR 2025 =====\n")
for i, trend in enumerate(result.pydantic.trends, 1):
    print(f"Trend {i}: {trend.trend_name}")
    print(f"Source: {trend.source_url}\n")

    # Ensure the trend is added to the database (just in case)
    if not trend_exists(trend.trend_name):
        add_trend(trend.trend_name, trend.source_url)

# Display all trends in database
print("\n===== ALL FASHION TRENDS IN DATABASE =====\n")
all_trends = get_all_trends()
for i, trend in enumerate(all_trends, 1):
    print(f"{i}. {trend['trend_name']}")
    print(f"   Source: {trend['source_url']}")
    print(f"   Discovered: {trend['discovered_date']}\n")

# Display all blocked URLs
print("\n===== BLOCKED URLS =====\n")
blocklist_path = 'config/blocked_urls.json'
try:
    with open(blocklist_path, 'r') as f:
        blocked_urls = json.load(f)

    if not blocked_urls:
        print("No URLs are currently blocked.")
    else:
        for i, url in enumerate(blocked_urls, 1):
            print(f"{i}. {url}")
except (FileNotFoundError, json.JSONDecodeError):
    print("No blocked URLs file found or file is invalid.")