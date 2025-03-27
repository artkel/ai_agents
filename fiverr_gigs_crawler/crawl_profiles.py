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
    print(f"\n=== Crawling fiverr profiles to {output_file_path} ===")

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
            f.write("# Fiverr profiles\n\n")
            f.write("This file contains the profile information crawled from the Fiverr website.\n\n")

            # Add a table of contents
            #f.write("## Table of Contents\n\n")

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

fiverr_gig_urls = [

    "https://www.fiverr.com/jasper_flow/build-ios-and-android-mobile-app-using-flutterflow?context_referrer=search_gigs_with_sellers_who_speak&source=drop_down_filters&ref_ctx_id=2c7e099658d348af93110e42292273c9&pckg_id=1&pos=2&ad_key=c0246e03-177f-4288-a8a6-dec232608061&context_type=auto&funnel=2c7e099658d348af93110e42292273c9&ref=leaf_category%3A520&seller_online=true&imp_id=327f85c8-4e30-4db7-912b-9c53d1172cfc",
    "https://www.fiverr.com/umair_alii/create-rag-application-using-llms-huggingface-gpt-and-langchain?context_referrer=search_gigs_with_sellers_who_speak&source=drop_down_filters&ref_ctx_id=2c7e099658d348af93110e42292273c9&pckg_id=1&pos=5&context_type=auto&funnel=2c7e099658d348af93110e42292273c9&ref=leaf_category%3A520&seller_online=true&fiverr_choice=true&imp_id=d2d93996-078a-416b-8ebc-d477daca5652",
    "https://www.fiverr.com/code_craf/do-ai-sass-ai-website-ai-app-developer-ai-agent-ai-chatbot-custom-ai-llm?context_referrer=search_gigs_with_sellers_who_speak&source=drop_down_filters&ref_ctx_id=2c7e099658d348af93110e42292273c9&pckg_id=1&pos=1&ad_key=c0246e03-177f-4288-a8a6-dec232608061&context_type=auto&funnel=2c7e099658d348af93110e42292273c9&ref=leaf_category%3A520&seller_online=true&imp_id=1fc59536-6d8f-41ea-98be-a0afcf284336",
    "https://www.fiverr.com/thomas_novamind/create-a-ai-sms-conversational-agent-book-appointment-customer-support?context_referrer=search_gigs_with_sellers_who_speak&source=drop_down_filters&ref_ctx_id=2c7e099658d348af93110e42292273c9&pckg_id=1&pos=3&ad_key=c0246e03-177f-4288-a8a6-dec232608061&context_type=auto&funnel=2c7e099658d348af93110e42292273c9&ref=leaf_category%3A520&imp_id=93851b6f-bf95-40d2-a706-6bb1616831c9",
    "https://www.fiverr.com/renu90/ai-agent-rag-automation-gen-ai-relevance-n8n-vapi-crew-ai-calling?context_referrer=search_gigs_with_sellers_who_speak&source=drop_down_filters&ref_ctx_id=2c7e099658d348af93110e42292273c9&pckg_id=1&pos=6&context_type=auto&funnel=2c7e099658d348af93110e42292273c9&ref=leaf_category%3A520&seller_online=true&imp_id=d41696d3-f2e2-47c5-a75d-e003c36a92b0",
    "https://www.fiverr.com/fizafatima617/build-ai-agents-for-automation-to-boost-your-business?context_referrer=search_gigs_with_sellers_who_speak&source=drop_down_filters&ref_ctx_id=2c7e099658d348af93110e42292273c9&pckg_id=1&pos=7&context_type=auto&funnel=2c7e099658d348af93110e42292273c9&ref=leaf_category%3A520&imp_id=90002fb8-dddb-4611-820a-7110a3e49cd4",
    "https://www.fiverr.com/king_automation/create-an-ai-agent-to-do-any-task?context_referrer=search_gigs_with_sellers_who_speak&source=drop_down_filters&ref_ctx_id=2c7e099658d348af93110e42292273c9&pckg_id=1&pos=9&ad_key=c0246e03-177f-4288-a8a6-dec232608061&context_type=auto&funnel=2c7e099658d348af93110e42292273c9&ref=leaf_category%3A520&imp_id=33da0bf6-92dd-4747-b883-6dbd8f5ff012",
    "https://www.fiverr.com/hanzala_webdev/make-an-ai-chatbot-using-botpress-stack-ai-and-zapier-as-ai-automation-agency?context_referrer=gig_page&source=similar_gigs&ref_ctx_id=b5bf37033a544d2db5cb09f19342bf5e&context=recommendation&pckg_id=1&pos=2&mod=ff&context_alg=t2g_dfm&imp_id=5e4ae2e9-1e6f-4edf-9488-894ad4901783",
    "https://www.fiverr.com/genixpro/build-you-a-question-answering-knowledge-chatbot?context_referrer=search_gigs_with_sellers_who_speak&source=drop_down_filters&ref_ctx_id=2c7e099658d348af93110e42292273c9&pckg_id=1&pos=12&ad_key=c0246e03-177f-4288-a8a6-dec232608061&context_type=auto&funnel=2c7e099658d348af93110e42292273c9&ref=leaf_category%3A520&imp_id=5abaca74-f73c-4e17-9638-79fa7ca62d45",
    "https://www.fiverr.com/husnain_zahoor/build-nlp-chatbots-llm-tts-stt-and-text-generation-apps?context_referrer=search_gigs_with_sellers_who_speak&source=drop_down_filters&ref_ctx_id=2c7e099658d348af93110e42292273c9&pckg_id=1&pos=19&ad_key=c0246e03-177f-4288-a8a6-dec232608061&context_type=auto&funnel=2c7e099658d348af93110e42292273c9&ref=leaf_category%3A520&imp_id=50272ad5-b37a-4d3e-95d3-981050069b3f",
    "https://www.fiverr.com/ahmadraza476/set-up-a-powerful-ai-cold-calling-agent-to-boost-your-sales?context_referrer=search_gigs_with_sellers_who_speak&source=drop_down_filters&ref_ctx_id=2c7e099658d348af93110e42292273c9&pckg_id=1&pos=31&ad_key=c0246e03-177f-4288-a8a6-dec232608061&context_type=auto&funnel=2c7e099658d348af93110e42292273c9&ref=leaf_category%3A520&imp_id=ba02d9ce-81d1-4238-ba21-9e2be3739de9",
    "https://www.fiverr.com/aviral_ai/build-a-custom-ai-agent-tailored-to-your-needs?context_referrer=search_gigs_with_sellers_who_speak&source=drop_down_filters&ref_ctx_id=2c7e099658d348af93110e42292273c9&pckg_id=1&pos=30&ad_key=c0246e03-177f-4288-a8a6-dec232608061&context_type=auto&funnel=2c7e099658d348af93110e42292273c9&ref=leaf_category%3A520&imp_id=d766ef8c-0c46-4ed4-85e9-b356231f21b4",
    "https://www.fiverr.com/leo_nassim/create-ai-agent-chatbot-with-langchain-gpt4o-claude-anthropic-saas-app?context_referrer=search_gigs_with_sellers_who_speak&source=drop_down_filters&ref_ctx_id=2c7e099658d348af93110e42292273c9&pckg_id=1&pos=38&context_type=auto&funnel=2c7e099658d348af93110e42292273c9&ref=leaf_category%3A520&imp_id=8bbed4ae-4319-41bd-bcf2-e46fcd973bca",
    "https://www.fiverr.com/codeplex/code-anything-web-and-mobile?context_referrer=search_gigs_with_sellers_who_speak&source=drop_down_filters&ref_ctx_id=2c7e099658d348af93110e42292273c9&pckg_id=1&pos=42&ad_key=c0246e03-177f-4288-a8a6-dec232608061&context_type=auto&funnel=2c7e099658d348af93110e42292273c9&ref=leaf_category%3A520&seller_online=true&imp_id=c9c437c3-b762-446d-adb8-bcb197cdefed",
    "https://www.fiverr.com/deeplearningdev/build-ai-agents-with-crewai-autogen-langchain-using-llm-gpt4-llama-claude-gemini?context_referrer=search_gigs_with_sellers_who_speak&source=drop_down_filters&ref_ctx_id=2c7e099658d348af93110e42292273c9&pckg_id=1&pos=40&context_type=auto&funnel=2c7e099658d348af93110e42292273c9&ref=leaf_category%3A520&imp_id=a61cd6bd-b90b-4216-abec-aa96c43512b6",

]

async def main():
    # Define the output file path
    output_file = os.path.join(__output__, "fiverr_profiles_raw.md")

    urls = fiverr_gig_urls
    if urls:
        print(f"Found {len(urls)} URLs to crawl")
        await crawl_and_save_to_single_file(urls, output_file, max_concurrent=10)
    else:
        print("No URLs found to crawl")


if __name__ == "__main__":
    asyncio.run(main())