# Warning control
import warnings
warnings.filterwarnings('ignore')
import os, yaml
import re
from dotenv import load_dotenv
from typing import List, Optional
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
import sqlite3

load_dotenv()
# Set up API keys
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Define Pydantic models for structured output
class FashionTrend(BaseModel):
    trend_name: str = Field(description="The exact name of the fashion trend as mentioned in the article")
    source_url: str = Field(description="URL of the article where the trend was found")
   # context: str = Field(description="The sentence or paragraph where the trend is mentioned")

class FashionTrends(BaseModel):
    trends: List[FashionTrend] = Field(description="List of three verified fashion trends from different sources")

class TrendDatabaseInput(BaseModel):
    """Input schema for TrendDatabaseTool."""
    action: str = Field(..., description="Action to perform: 'check', 'add', or 'list'")
    trend_name: Optional[str] = Field(None, description="Name of the trend to check or add")
    source_url: Optional[str] = Field(None, description="URL source for the trend")

# set up database
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

#create db functions
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
# ... and db tool
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
search_tool = SerperDevTool(n_results=20)  # Increased results as mentioned
scrape_tool = ScrapeWebsiteTool(text_content=True)  # Only get text content to reduce tokensv
db_tool = TrendDatabaseTool()

# Create a fashion researcher agent with all tools
fashion_researcher = Agent(
    role="Fashion Trend Researcher and Verifier",
    goal="Find and verify new women's fashion trends for 2025 that haven't been discovered before",
    backstory="""You are an expert fashion researcher who stays on top of upcoming trends. 
    Your specialty is identifying emerging women's fashion trends from reliable sources.
    You are also meticulous about verifying information and ensuring you don't duplicate trends.""",
    tools=[search_tool, scrape_tool, db_tool],
    verbose=True,
    llm="openai/gpt-4o-mini-2024-07-18"
)

# Create an enhanced search and verification task with database checks
fashion_task = Task(
    description="""
    Your task is to find new, verified women's fashion trends for 2025 that aren't already in our database:

    1. First, use the database tool with 'list' action to see what trends we already know about

    2. Then, search for these exact keywords to find potential new trends:
       - "Women fashion trends 2025"
       - "Women's clothing trends 2025"
       - "New women's style 2025"

    3. For each potential trend you find:
       - Check if it already exists in our database using the 'check' action
       - If it does exist, skip it and look for another trend
       - If it's new, use the scraping tool to verify that the trend actually appears in the article
       - If verified, add it to your findings

    4. Once you verify a trend that's not in our database, use the 'add' action to add it

    5. Continue until you have found THREE different new verified trends

    Your final output should be exactly three new verified fashion trends in the required format.

    IMPORTANT VERIFICATION RULES:
    - A trend is only considered verified if the exact trend name appears in the article content
    - IMPORTANT: Each trend must come from a different source (different URLs)
    - Avoid awellstyledlife web source. FDo not pick up trends from this website.
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