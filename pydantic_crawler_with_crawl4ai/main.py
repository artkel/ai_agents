import os
import sys
import psutil
import asyncio
import requests
from xml.etree import ElementTree
from urllib.parse import urlparse

__location__ = os.path.dirname(os.path.abspath(__file__))
__output__ = os.path.join(__location__, "output")

# Create output directory if it doesn't exist
os.makedirs(__output__, exist_ok=True)

# Append parent directory to system path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from typing import List, Dict
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode


def get_filename_from_url(url: str) -> str:
    """Generate a valid filename from a URL."""
    parsed = urlparse(url)
    # Remove the domain and use the path
    path = parsed.path.strip('/')

    # Replace forward slashes with underscores
    path = path.replace('/', '_')

    # If the path is empty (e.g., for domain.com/), use 'index'
    if not path:
        path = 'index'

    # If the path doesn't end with .md, add it
    if not path.endswith('.md'):
        path += '.md'

    return path


async def crawl_parallel(urls: List[str], max_concurrent: int = 3) -> Dict[str, str]:
    print("\n=== Parallel Crawling with Browser Reuse + Memory Check ===")

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
                        # Add URL as title at the beginning of the markdown if not already present
                        title_md = f"# {url}\n\n"
                        if not markdown_content.startswith(f"# {url}"):
                            markdown_content = title_md + markdown_content

                        # Store in our dictionary
                        crawled_content[url] = markdown_content

                        # Save individual files
                        filename = get_filename_from_url(url)
                        file_path = os.path.join(__output__, filename)

                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(markdown_content)

                        print(f"Saved markdown for {url} to {file_path}")
                    else:
                        print(f"No markdown content for {url}")
                else:
                    fail_count += 1
                    print(f"Failed to crawl {url}: {result.error if hasattr(result, 'error') else 'Unknown error'}")

        print(f"\nSummary:")
        print(f"  - Successfully crawled: {success_count}")
        print(f"  - Failed: {fail_count}")

        # Save all content to a single markdown file
        combined_markdown_path = os.path.join(__output__, "pydantic_docs_combined.md")
        with open(combined_markdown_path, 'w', encoding='utf-8') as f:
            f.write("# Pydantic AI Documentation\n\n")
            f.write("This file contains the combined documentation crawled from the Pydantic website.\n\n")

            # Add a table of contents
            f.write("## Table of Contents\n\n")
            for url in crawled_content.keys():
                f.write(f"- [{url}](#{urlparse(url).path.replace('/', '-')})\n")

            f.write("\n---\n\n")

            # Write all the content
            for url, content in crawled_content.items():
                f.write(f"<a id='{urlparse(url).path.replace('/', '-')}'></a>\n\n")
                f.write(content)
                f.write("\n\n---\n\n")

        print(f"\nCombined markdown saved to {combined_markdown_path}")
        return crawled_content

    finally:
        print("\nClosing crawler...")
        await crawler.close()
        # Final memory log
        log_memory(prefix="Final: ")
        print(f"\nPeak memory usage (MB): {peak_memory // (1024 * 1024)}")


def get_pydantic_ai_docs_urls():
    """
    Fetches all URLs from the Pydantic AI documentation.
    Uses the sitemap (https://docs.pydantic.dev/latest/sitemap.xml ) to get these URLs.

    Returns:
        List[str]: List of URLs
    """
    sitemap_url = "https://docs.pydantic.dev/latest/sitemap.xml"
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()

        # Parse the XML
        root = ElementTree.fromstring(response.content)

        # Extract all URLs from the sitemap
        # The namespace is usually defined in the root element
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = [loc.text for loc in root.findall('.//ns:loc', namespace)]

        return urls
    except Exception as e:
        print(f"Error fetching sitemap: {e}")
        return []


async def main():
    urls = get_pydantic_ai_docs_urls()
    if urls:
        print(f"Found {len(urls)} URLs to crawl")
        await crawl_parallel(urls, max_concurrent=10)
    else:
        print("No URLs found to crawl")


if __name__ == "__main__":
    asyncio.run(main())