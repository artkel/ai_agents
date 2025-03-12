import os
import sys
import psutil
import asyncio
import requests
from xml.etree import ElementTree
from urllib.parse import urlparse
import re

__location__ = os.path.dirname(os.path.abspath(__file__))
__output__ = os.path.join(__location__, "output")

# Create output directory if it doesn't exist
os.makedirs(__output__, exist_ok=True)

# Append parent directory to system path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from typing import List, Dict
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode


def get_readable_title_from_url(url: str) -> str:
    """Generate a readable title from a URL."""
    parsed = urlparse(url)
    # Remove the domain and use the path
    path = parsed.path.strip('/')

    if not path:
        return "Home"

    # Split by slashes and get the last part
    parts = path.split('/')
    title = parts[-1]

    # Replace hyphens and underscores with spaces
    title = title.replace('-', ' ').replace('_', ' ')

    # Capitalize words
    title = ' '.join(word.capitalize() for word in title.split())

    return title


async def crawl_and_save_to_single_file(urls: List[str], output_file_path: str, max_concurrent: int = 3) -> bool:
    print(f"\n=== Crawling Crew AI Documentation to {output_file_path} ===")

    # We'll keep track of peak memory usage across all tasks
    peak_memory = 0
    process = psutil.Process(os.getpid())

    # Dictionary to store the crawled content
    crawled_content = {}

    def log_memory(prefix: str = ""):
        nonlocal peak_memory
        current_mem = process.memory_info().rss  # in bytes
        if current_mem > peak_memory:
            peak_memory = current_mem
        print(f"{prefix} Current Memory: {current_mem // (1024 * 1024)} MB, Peak: {peak_memory // (1024 * 1024)} MB")

    # Minimal browser config
    browser_config = BrowserConfig(
        headless=True,
        verbose=False,
        extra_args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"],
    )
    crawl_config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS)

    # Create the crawler instance
    crawler = AsyncWebCrawler(config=browser_config)
    await crawler.start()

    try:
        # We'll chunk the URLs in batches of 'max_concurrent'
        success_count = 0
        fail_count = 0
        for i in range(0, len(urls), max_concurrent):
            batch = urls[i: i + max_concurrent]
            tasks = []

            for j, url in enumerate(batch):
                # Unique session_id per concurrent sub-task
                session_id = f"parallel_session_{i + j}"
                task = crawler.arun(url=url, config=crawl_config, session_id=session_id)
                tasks.append(task)

            # Check memory usage prior to launching tasks
            log_memory(prefix=f"Before batch {i // max_concurrent + 1}: ")

            # Gather results
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Check memory usage after tasks complete
            log_memory(prefix=f"After batch {i // max_concurrent + 1}: ")

            # Evaluate results
            for url, result in zip(batch, results):
                if isinstance(result, Exception):
                    print(f"Error crawling {url}: {result}")
                    fail_count += 1
                elif result.success:
                    success_count += 1

                    # Get the markdown content directly from Crawl4AI
                    markdown_content = result.markdown

                    if markdown_content:
                        # Get a readable title for the section
                        title = get_readable_title_from_url(url)

                        # Store in our dictionary with title and URL info
                        crawled_content[url] = {
                            'title': title,
                            'content': markdown_content
                        }
                    else:
                        print(f"No markdown content for {url}")
                else:
                    fail_count += 1
                    print(f"Failed to crawl {url}: {result.error if hasattr(result, 'error') else 'Unknown error'}")

        print(f"\nSummary:")
        print(f"  - Successfully crawled: {success_count}")
        print(f"  - Failed: {fail_count}")

        # Sort URLs by path depth (top-level pages first)
        sorted_urls = sorted(crawled_content.keys(),
                             key=lambda url: (len(urlparse(url).path.split('/')), url))

        # Save all content to a single markdown file
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write("# Crew AI Documentation\n\n")
            f.write("This file contains the combined documentation crawled from the CrewAI website.\n\n")

            # Add a table of contents
            f.write("## Table of Contents\n\n")

            # Track sections for multi-level TOC
            current_section = None

            for url in sorted_urls:
                parsed = urlparse(url)
                path_parts = parsed.path.strip('/').split('/')

                title = crawled_content[url]['title']
                anchor = re.sub(r'[^a-zA-Z0-9_-]', '', title.lower().replace(' ', '-'))

                # Handle multi-level TOC for better organization
                if len(path_parts) == 0 or path_parts[0] == '':
                    # Home page
                    f.write(f"- [Home](#{anchor})\n")
                    current_section = None
                elif len(path_parts) == 1:
                    # Top-level section
                    f.write(f"- [{title}](#{anchor})\n")
                    current_section = path_parts[0]
                else:
                    # Nested section
                    indent = "  " * (len(path_parts) - 1)
                    f.write(f"{indent}- [{title}](#{anchor})\n")

            f.write("\n---\n\n")

            # Write all the content
            for url in sorted_urls:
                title = crawled_content[url]['title']
                content = crawled_content[url]['content']

                # Create an anchor ID for linking
                anchor = re.sub(r'[^a-zA-Z0-9_-]', '', title.lower().replace(' ', '-'))

                f.write(f"<a id='{anchor}'></a>\n\n")
                f.write(f"## {title}\n\n")
                f.write(f"*Source: [{url}]({url})*\n\n")

                # Clean up and add the content
                # Remove the title if it already exists in the content
                title_pattern = re.compile(r'^# .*\n', re.MULTILINE)
                if title_pattern.match(content):
                    content = title_pattern.sub('', content, 1)

                f.write(content)
                f.write("\n\n---\n\n")

        print(f"\nDocumentation saved to {output_file_path}")
        return True

    finally:
        print("\nClosing crawler...")
        await crawler.close()
        # Final memory log
        log_memory(prefix="Final: ")
        print(f"\nPeak memory usage (MB): {peak_memory // (1024 * 1024)}")

# def get_pydantic_ai_docs_urls():
#     """
#     Fetches all URLs from the Pydantic AI documentation.
#     Uses the sitemap (https://ai.pydantic.dev/sitemap.xml) to get these URLs.
#
#     Returns:
#         List[str]: List of URLs
#     """
#     sitemap_url = "https://ai.pydantic.dev/sitemap.xml"
#     try:
#         response = requests.get(sitemap_url)
#         response.raise_for_status()
#
#         # Parse the XML
#         root = ElementTree.fromstring(response.content)
#
#         # Extract all URLs from the sitemap
#         # The namespace is usually defined in the root element
#         namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
#         urls = [loc.text for loc in root.findall('.//ns:loc', namespace)]
#
#         return urls
#     except Exception as e:
#         print(f"Error fetching sitemap: {e}")
#         return []

crewai_documentation_urls = [
    # get started
    "https://docs.crewai.com/introduction",
    "https://docs.crewai.com/installation",
    "https://docs.crewai.com/quickstart",

    # core concepts
    "https://docs.crewai.com/concepts/agents",
    "https://docs.crewai.com/concepts/tasks",
    "https://docs.crewai.com/concepts/crews",
    "https://docs.crewai.com/concepts/flows",
    "https://docs.crewai.com/concepts/knowledge",
    "https://docs.crewai.com/concepts/llms",
    "https://docs.crewai.com/concepts/processes",
    "https://docs.crewai.com/concepts/collaboration",
    "https://docs.crewai.com/concepts/training",
    "https://docs.crewai.com/concepts/memory",
    "https://docs.crewai.com/concepts/planning",
    "https://docs.crewai.com/concepts/testing",
   # "https://docs.crewai.com/concepts/cli",
    "https://docs.crewai.com/concepts/tools",

    # how to guides
    "https://docs.crewai.com/how-to/create-custom-tools",
    "https://docs.crewai.com/how-to/sequential-process",
    "https://docs.crewai.com/how-to/hierarchical-process",
    "https://docs.crewai.com/how-to/custom-manager-agent",
    "https://docs.crewai.com/how-to/llm-connections",
    "https://docs.crewai.com/how-to/customizing-agents",
    "https://docs.crewai.com/how-to/multimodal-agents",
    "https://docs.crewai.com/how-to/coding-agents",
    "https://docs.crewai.com/how-to/force-tool-output-as-result",
    "https://docs.crewai.com/how-to/human-input-on-execution",
    "https://docs.crewai.com/how-to/kickoff-async",
    "https://docs.crewai.com/how-to/kickoff-for-each",
    "https://docs.crewai.com/how-to/replay-tasks-from-latest-crew-kickoff",
    "https://docs.crewai.com/how-to/conditional-tasks",
    #"https://docs.crewai.com/how-to/agentops-observability",
    #"https://docs.crewai.com/how-to/langtrace-observability",

    # tools
    "https://docs.crewai.com/tools/aimindtool",
    "https://docs.crewai.com/tools/bravesearchtool",
    "https://docs.crewai.com/tools/browserbaseloadtool",
    #"https://docs.crewai.com/tools/codedocssearchtool",
    "https://docs.crewai.com/tools/codeinterpretertool",
    #"https://docs.crewai.com/tools/composiotool",
    #"https://docs.crewai.com/tools/csvsearchtool",
    "https://docs.crewai.com/tools/dalletool",
    #"https://docs.crewai.com/tools/directorysearchtool",
    #"https://docs.crewai.com/tools/docxsearchtool",
    #"https://docs.crewai.com/tools/filereadtool",
    #"https://docs.crewai.com/tools/filewritetool",
    #"https://docs.crewai.com/tools/firecrawlcrawlwebsitetool",
    #"https://docs.crewai.com/tools/firecrawlscrapewebsitetool",
    #"https://docs.crewai.com/tools/firecrawlsearchtool",
    #"https://docs.crewai.com/tools/githubsearchtool",
    "https://docs.crewai.com/tools/serperdevtool",
    "https://docs.crewai.com/tools/jsonsearchtool",
    #"https://docs.crewai.com/tools/pdfsearchtool",
    "https://docs.crewai.com/tools/scrapflyscrapetool",
    "https://docs.crewai.com/tools/websitesearchtool"

]

async def main():
    # Define the output file path
    output_file = os.path.join(__output__, "crewai_documentation_raw.md")

    urls = crewai_documentation_urls
    if urls:
        print(f"Found {len(urls)} URLs to crawl")
        await crawl_and_save_to_single_file(urls, output_file, max_concurrent=10)
    else:
        print("No URLs found to crawl")


if __name__ == "__main__":
    asyncio.run(main())