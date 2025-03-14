from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import requests
import os, re, json
from pathlib import Path
from dotenv import load_dotenv
from crewai_tools import SerperDevTool
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Optional

# Load environment variables
load_dotenv()


# Custom Spider Crawler Tool
class SpiderCrawlerInput(BaseModel):
    url: str = Field(..., description="The URL of the fashion article to crawl")
    trend_name: str = Field(..., description="The exact name of the trend to extract from the article")
    chars_to_extract: int = Field(1000, description="Number of characters to extract after finding the trend")
    limit: int = Field(1, description="The number of pages to crawl")
    readability: bool = Field(True, description="Whether to extract the readable content")
    return_format: str = Field("markdown", description="The format to return the content in")

class UltraMinimalInput(BaseModel):
    url: str = Field(..., description="The URL of the fashion article to crawl")
    trend_name: str = Field(..., description="The exact name of the trend to extract from the article")

class EfficientSearchTool(SerperDevTool):
    """A more efficient version of SerperDevTool that limits result size."""

    def run(self, search_query: str, country: Optional[str] = None, n_results: int = 5, save_file: bool = False):
        """Run the search with limited results."""
        # Use parent class to perform search but with fewer results
        results = super().run(search_query=search_query, country=country, n_results=n_results, save_file=save_file)

        # Further limit the output to avoid token issues
        limited_results = self._limit_results(results)

        return limited_results

    def _limit_results(self, results: str) -> str:
        """Limit the size of each search result."""
        lines = results.split("\n")
        limited_lines = []

        for line in lines:
            # Keep title lines (they start with "Title:")
            if line.startswith("Title:"):
                limited_lines.append(line)
            # Keep link lines but don't truncate them
            elif line.startswith("Link:"):
                limited_lines.append(line)
            # Limit snippet lines to 100 characters
            elif line.startswith("Snippet:"):
                parts = line.split(":", 1)
                if len(parts) > 1:
                    snippet = parts[1].strip()
                    if len(snippet) > 100:
                        snippet = snippet[:100] + "..."
                    limited_lines.append(f"Snippet: {snippet}")
            # Include separator lines
            elif line.startswith("---"):
                limited_lines.append(line)

        return "\n".join(limited_lines)


class UltraMinimalCrawlerTool(BaseTool):
    name: str = "UltraMinimalCrawlerTool"
    description: str = """
    Extract essential trend information and relevant images from fashion articles.
    """
    args_schema: Type[BaseModel] = UltraMinimalInput

    def _run(self, url: str, trend_name: str) -> str:
        SPIDER_API_KEY = os.getenv("SPIDER_API_KEY")

        if not SPIDER_API_KEY:
            return "Error: SPIDER_API_KEY environment variable is missing"

        headers = {
            'Authorization': f'Bearer {SPIDER_API_KEY}',
            'Content-Type': 'application/json'
        }

        # First request: Get markdown content for text extraction
        json_data_markdown = {
            "limit": 1,
            "readability": True,
            "url": url,
            "return_format": "markdown"
        }

        try:
            # Get markdown for text analysis
            markdown_response = requests.post(
                'https://api.spider.cloud/crawl',
                headers=headers,
                json=json_data_markdown
            )

            if markdown_response.status_code == 200:
                markdown_result = markdown_response.json()

                if markdown_result and len(markdown_result) > 0:
                    # Extract the trend section using your proven function
                    markdown_content = markdown_result[0]['content']
                    trend_section = self.extract_trend_section(markdown_content, trend_name, 1500)

                    # Extract image URLs from markdown content
                    markdown_image_urls = self.extract_markdown_images(trend_section)

                    # Produce final output
                    output = f"TREND: {trend_name}\n\n"
                    output += f"ARTICLE URL: {url}\n\n"
                    output += f"TREND SECTION:\n{trend_section[:1000]}..."  # Limit to 1000 chars

                    if markdown_image_urls:
                        output += f"\n\nIMAGE URLS (FROM MARKDOWN):\n"
                        for img_url in markdown_image_urls[:2]:
                            output += f"- {img_url}\n"
                    else:
                        output += "\n\nNo images found in the trend section."

                    return output
                else:
                    return "No content found in the response"
            else:
                return f"Error with markdown request: {markdown_response.status_code}"

        except Exception as e:
            return f"Error processing article: {str(e)}"

    def extract_trend_section(self, full_content, trend_name, chars_to_extract=1000):
        """
        Extract a section around a trend name, focusing on actual headings.
        Also includes context before the heading when possible.
        """
        import re

        # Split the content into lines
        lines = full_content.split('\n')

        # Look for the trend name in markdown headings (# Heading)
        heading_pattern = re.compile(r'^(#+)\s+(.*?)$')

        found_line_index = -1
        is_heading = False

        # First, try to find the trend name in a markdown heading
        for i, line in enumerate(lines):
            match = heading_pattern.match(line)
            if match and trend_name.lower() in match.group(2).lower():
                found_line_index = i
                is_heading = True
                break

        # If not found in headings, look for the trend name anywhere
        if found_line_index == -1:
            for i, line in enumerate(lines):
                if trend_name.lower() in line.lower():
                    found_line_index = i
                    break

        # If still not found, return an error
        if found_line_index == -1:
            return f"Error: Could not find trend '{trend_name}' in the article."

        # Now extract the content - including context before the heading when possible
        result = []

        # Add context from lines before the found line (up to 30 chars worth)
        if found_line_index > 0:
            chars_before = 0
            context_lines = []

            # Go backward from the found line until we have about 30 chars
            for j in range(found_line_index - 1, max(0, found_line_index - 5), -1):
                line = lines[j]
                context_lines.insert(0, line)  # Insert at beginning to maintain order
                chars_before += len(line)

                if chars_before >= 30:
                    break

            # Add the context lines to the result
            result.extend(context_lines)

        # Add the found line
        result.append(lines[found_line_index])

        # If it's a heading, extract content until the next heading of same or higher level
        if is_heading:
            heading_level = len(heading_pattern.match(lines[found_line_index]).group(1))

            chars_count = len(lines[found_line_index])
            i = found_line_index + 1

            while i < len(lines) and chars_count < chars_to_extract:
                line = lines[i]
                heading_match = heading_pattern.match(line)

                # Stop if we hit another heading of same or higher level
                if heading_match and len(heading_match.group(1)) <= heading_level:
                    break

                result.append(line)
                chars_count += len(line)
                i += 1
        else:
            # Not a heading, just extract a certain number of characters
            chars_count = len(lines[found_line_index])
            i = found_line_index + 1

            while i < len(lines) and chars_count < chars_to_extract:
                result.append(lines[i])
                chars_count += len(lines[i])
                i += 1

        # Join the lines back together
        return '\n'.join(result)

    def extract_markdown_images(self, markdown_content):
        """Extract image URLs from markdown content."""
        import re

        # Pattern to match markdown image syntax: ![alt text](URL)
        image_pattern = r'!\[.*?\]\((https?://[^\s\)]+)\)'

        # Find all image URLs
        image_urls = re.findall(image_pattern, markdown_content)

        return image_urls

class SpiderCrawlerTool(BaseTool):
    name: str = "SpiderCrawlerTool"
    description: str = """
    Use this tool to crawl fashion articles and extract specific trend sections.
    Provide the URL of a fashion article and the exact trend name, and this tool will return 
    only the relevant section about that trend including its description and images.
    """
    args_schema: Type[BaseModel] = SpiderCrawlerInput

    def _run(
            self,
            url: str,
            trend_name: str,
            chars_to_extract: int = 1000,
            limit: int = 1,
            readability: bool = True,
            return_format: str = "markdown"
    ) -> str:
        SPIDER_API_KEY = os.getenv("SPIDER_API_KEY")

        if not SPIDER_API_KEY:
            return "Error: SPIDER_API_KEY environment variable is missing"

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
                    # Get the content
                    full_content = result[0]['content'].rstrip()
                    article_url = result[0]['url']

                    # Extract the trend section
                    trend_section = self.extract_trend_section(full_content, trend_name, chars_to_extract)

                    # Extract image URLs from the trend section
                    image_urls = self.extract_image_urls(trend_section)

                    return f"URL: {article_url}\n\nTREND SECTION:\n{trend_section}\n\nIMAGE URLS:\n{image_urls}"
                else:
                    return "No content found in the response"
            else:
                return f"Error: {response.status_code}\n{response.text}"

        except Exception as e:
            return f"Error crawling the URL: {str(e)}"

    def extract_trend_section(self, full_content, trend_name, chars_to_extract=1000):
        """
        Extract a section around a trend name, focusing on actual headings.
        """
        # Split the content into lines
        lines = full_content.split('\n')

        # Look for the trend name in markdown headings (# Heading)
        heading_pattern = re.compile(r'^(#+)\s+(.*?)$')

        found_line_index = -1
        is_heading = False

        # First, try to find the trend name in a markdown heading
        for i, line in enumerate(lines):
            match = heading_pattern.match(line)
            if match and trend_name.lower() in match.group(2).lower():
                found_line_index = i
                is_heading = True
                break

        # If not found in headings, look for the trend name anywhere
        if found_line_index == -1:
            for i, line in enumerate(lines):
                if trend_name.lower() in line.lower():
                    found_line_index = i
                    break

        # If still not found, return an error
        if found_line_index == -1:
            return f"Error: Could not find trend '{trend_name}' in the article."

        # Now extract the content - if it's a heading, include content until the next heading
        # or up to chars_to_extract characters
        result = []

        # Add the found line
        result.append(lines[found_line_index])

        # If it's a heading, extract content until the next heading of same or higher level
        if is_heading:
            heading_level = len(heading_pattern.match(lines[found_line_index]).group(1))

            chars_count = len(lines[found_line_index])
            i = found_line_index + 1

            while i < len(lines) and chars_count < chars_to_extract:
                line = lines[i]
                heading_match = heading_pattern.match(line)

                # Stop if we hit another heading of same or higher level
                if heading_match and len(heading_match.group(1)) <= heading_level:
                    break

                result.append(line)
                chars_count += len(line)
                i += 1
        else:
            # Not a heading, just extract a certain number of characters
            chars_count = len(lines[found_line_index])
            i = found_line_index + 1

            while i < len(lines) and chars_count < chars_to_extract:
                result.append(lines[i])
                chars_count += len(lines[i])
                i += 1

        # Join the lines back together
        return '\n'.join(result)

    def extract_image_urls(self, content):
        """Extract image URLs from markdown content."""
        # Find markdown image syntax: ![alt text](URL)
        image_urls = re.findall(r'!\[.*?\]\((https?://[^\s\)]+)\)', content)

        if not image_urls:
            return "No images found in the trend section."

        return "\n".join([f"- {url}" for url in image_urls])


@CrewBase
class FashionTrendsCrew:
    """Crew for extracting and reporting on women's fashion trends for 2025"""

    @agent
    def search_agent(self) -> Agent:
        # Use our custom efficient search tool with fewer results
        efficient_search_tool = EfficientSearchTool()

        return Agent(
            config=self.agents_config['search_agent'],
            tools=[efficient_search_tool],
            verbose=True
        )

    @agent
    def crawler_agent(self) -> Agent:
        # Use the ultra-minimal tool for extraction
        ultra_minimal_tool = UltraMinimalCrawlerTool()

        return Agent(
            config=self.agents_config['crawler_agent'],
            tools=[ultra_minimal_tool],
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