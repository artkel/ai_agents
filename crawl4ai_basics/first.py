import os, sys, psutil, asyncio, requests, re
from xml.etree import ElementTree
from urllib.parse import urlparse
from typing import List, Dict
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator



__location__ = os.path.dirname(os.path.abspath(__file__))
__output__ = os.path.join(__location__, "output")

# Create output directory if it doesn't exist
os.makedirs(__output__, exist_ok=True)

# Append parent directory to system path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)


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
    print(f"\n=== Crawling Web Data to {output_file_path} ===")

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

    md_generator = DefaultMarkdownGenerator(
        content_filter=PruningContentFilter(
            threshold=.4, # Any content section with a relevance score below 0.4 will be removed
            threshold_type="fixed" # "adaptive
        )
    )

    crawl_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        # markdown_generator=md_generator
    )

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


urls_to_crawl = [
    "https://cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions#extract"
]

async def main():
    # Define the output file path
    output_file = os.path.join(__output__, "crawled_data.md")

    urls = urls_to_crawl
    if urls:
        print(f"Found {len(urls)} URLs to crawl")
        await crawl_and_save_to_single_file(urls, output_file, max_concurrent=10)
    else:
        print("No URLs found to crawl")


if __name__ == "__main__":
    asyncio.run(main())