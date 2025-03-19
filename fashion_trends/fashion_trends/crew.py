from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, output_pydantic
import datetime, os
from dotenv import load_dotenv
from .tools import search_tool, crawler_tool, scrape_tool, db_tool, blocklist_tool, setup_database
from .data_models import FashionTrends, CrawledTrends

# Load environment variables from .env file
load_dotenv()

# Access the API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# Set them explicitly in os.environ to ensure they're available to the libraries
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["SERPER_API_KEY"] = SERPER_API_KEY

setup_database()

@CrewBase
class FashionTrendsCrew:
    """Crew for extracting and reporting on women's fashion trends for 2025"""

    @agent
    def fashion_researcher(self) -> Agent:
        # Use our custom efficient search tool with fewer results

        return Agent(
            config=self.agents_config['fashion_researcher'],
            tools=[search_tool, scrape_tool, db_tool, blocklist_tool],
            verbose=True,
            output_pydantic=FashionTrends
        )

    @agent
    def crawler_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['crawler_agent'],
            tools=[crawler_tool],
            verbose=True,
            output_pydantic=CrawledTrends
        )

    @agent
    def report_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['report_agent'],
            verbose=True
        )

    @task
    def search_task(self) -> Task:
        return Task(
            config=self.tasks_config['search_task']
        )

    @task
    def crawl_task(self) -> Task:
        return Task(
            config=self.tasks_config['crawl_task']
        )

    @task
    def report_task(self) -> Task:
        timestamp = datetime.datetime.now().strftime("D%Y%m%dT%H%M")
        return Task(
            config=self.tasks_config['report_task'],
            output_file=f'output/fashion_trends_2025_{timestamp}.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Fashion Trends crew"""
        return Crew(
            agents=[
                self.fashion_researcher(),
                self.crawler_agent(),
                self.report_agent()
            ],
            tasks=[
                self.search_task(),
                self.crawl_task(),
                self.report_task()
            ],
            process=Process.sequential,
            verbose=True,
        )