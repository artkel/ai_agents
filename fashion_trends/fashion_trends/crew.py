from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import requests
import os
from dotenv import load_dotenv
from crewai_tools import SerperDevTool
from crewai.tools import BaseTool  # Use crewai.tools instead of langchain.tools
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, Type

# Load environment variables
load_dotenv()


# Custom Spider Crawler Tool
class SpiderCrawlerInput(BaseModel):
    url: str = Field(..., description="The URL of the article to crawl")
    trend_name: str = Field(..., description="The exact name of the trend to extract from the article")
    limit: int = Field(1, description="The number of pages to crawl")
    readability: bool = Field(True, description="Whether to extract the readable content")
    return_format: str = Field("markdown", description="The format to return the content in")

class SpiderCrawlerTool(BaseTool):
    name: str = "SpiderCrawlerTool"
    description: str = """
    Use this tool to crawl web articles and extract the section containing a specific trend.
    Provide the URL of a fashion article and the trend name, and this tool will return
    the trend section in markdown format.
    """
    args_schema: Type[BaseModel] = SpiderCrawlerInput

    def _run(self, url: str, trend_name: str = "", limit: int = 1, readability: bool = True,
             return_format: str = "markdown") -> str:
        SPIDER_API_KEY = os.getenv("SPIDER_API_KEY")

        if not SPIDER_API_KEY:
            return "Error: SPIDER_API_KEY environment variable is missing"

        # First, make sure we have a trend name to look for
        if not trend_name:
            return "Error: Please provide a trend name to search for in the article"

        headers = {
            'Authorization': f'Bearer {SPIDER_API_KEY}',
            'Content-Type': 'application/json'
        }

        json_data = {
            "limit": limit,
            "readability": readability,
            "url": url,
            "return_format": return_format
        }

        try:
            response = requests.post(
                'https://api.spider.cloud/crawl',
                headers=headers,
                json=json_data
            )

            if response.status_code == 200:
                result = response.json()
                if result and len(result) > 0:
                    full_content = result[0]['content']

                    # Find the trend name in the content
                    trend_index = full_content.find(trend_name)

                    if trend_index >= 0:
                        # Extract exactly 1000 characters after the trend name
                        chars_after_trend = 1000

                        # Include the trend name itself, some context before it, and chars_after_trend characters after it
                        context_before = 100  # Characters before the trend name for context
                        section_start = max(0, trend_index - context_before)
                        section_end = min(len(full_content), trend_index + len(trend_name) + chars_after_trend)

                        trend_section = full_content[section_start:section_end]

                        return f"URL: {result[0]['url']}\n\nTREND SECTION: {trend_section}"
                    else:
                        return f"Error: Could not find trend '{trend_name}' in the article. Please check the spelling."
                else:
                    return "No content found in the response"
            else:
                return f"Error: {response.status_code}\n{response.text}"

        except Exception as e:
            return f"Error crawling the URL: {str(e)}"

# class SpiderCrawlerTool(BaseTool):
#     name: str = "SpiderCrawlerTool"  # Add type annotation here
#     description: str = """
#     Use this tool to crawl web articles and extract content including text and images.
#     Provide the URL of a fashion article, and this tool will return the content in markdown format.
#     This is especially useful for extracting detailed information about fashion trends including images.
#     """  # Add type annotation here
#     args_schema: Type[BaseModel] = SpiderCrawlerInput  # Add type annotation here
#
#     def _run(self, url: str, limit: int = 1, readability: bool = True, return_format: str = "markdown") -> str:
#         SPIDER_API_KEY = os.getenv("SPIDER_API_KEY")
#
#         if not SPIDER_API_KEY:
#             return "Error: SPIDER_API_KEY environment variable is missing"
#
#         headers = {
#             'Authorization': f'Bearer {SPIDER_API_KEY}',
#             'Content-Type': 'application/json'
#         }
#
#         json_data = {
#             "limit": limit,
#             "readability": readability,
#             "url": url,
#             "return_format": return_format
#         }
#
#         try:
#             response = requests.post(
#                 'https://api.spider.cloud/crawl',
#                 headers=headers,
#                 json=json_data
#             )
#
#             if response.status_code == 200:
#                 result = response.json()
#                 if result and len(result) > 0:
#                     # Return both URL and content together
#                     return f"URL: {result[0]['url']}\n\nCONTENT: {result[0]['content']}"
#                 else:
#                     return "No content found in the response"
#             else:
#                 return f"Error: {response.status_code}\n{response.text}"
#
#         except Exception as e:
#             return f"Error crawling the URL: {str(e)}"


@CrewBase
class FashionTrendsCrew:
    """Crew for extracting and reporting on women's fashion trends for 2025"""

    # # Get the directory containing this file
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # # Go up one level to the project root
    # project_root = os.path.dirname(current_dir)
    #
    # # Absolute paths to config files
    # agents_config = os.path.join(project_root, "config", "agents.yaml")
    # tasks_config = os.path.join(project_root, "config", "tasks.yaml")

    @agent
    def search_agent(self) -> Agent:
        # Use SerperDevTool for web search
        serper_tool = SerperDevTool()

        return Agent(
            config=self.agents_config['search_agent'],
            tools=[serper_tool],
            verbose=True
        )

    @agent
    def crawler_agent(self) -> Agent:
        # Use custom Spider Crawler tool
        spider_tool = SpiderCrawlerTool()

        return Agent(
            config=self.agents_config['crawler_agent'],
            tools=[spider_tool],
            verbose=True
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
        return Task(
            config=self.tasks_config['report_task'],
            output_file='output/fashion_trends_2025.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Fashion Trends crew"""
        return Crew(
            agents=[
                self.search_agent(),
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