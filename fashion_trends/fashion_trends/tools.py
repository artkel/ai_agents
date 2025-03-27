from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from typing import List, Optional, Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from .data_models import CrawlerToolInput, BlocklistInput, TrendDatabaseInput
import os, json, requests, re, datetime, sqlite3

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

class EfficientSearchTool(SerperDevTool):
    """A more efficient version of SerperDevTool that limits result size."""

    def run(self, search_query: str, country: Optional[str] = None, n_results: int = 15, save_file: bool = False):
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
    args_schema: Type[BaseModel] = CrawlerToolInput

    def _run(self, url: str, trend_name: str) -> str:
        SPIDER_API_KEY = os.getenv("SPIDER_API_KEY")

        if not SPIDER_API_KEY:
            return "Error: SPIDER_API_KEY environment variable is missing"

        headers = {
            'Authorization': f'Bearer {SPIDER_API_KEY}',
            'Content-Type': 'application/json'
        }

        # Get HTML content
        json_data_html = {
            "limit": 1,
            "readability": False,
            "url": url,
            "return_format": "html"
        }

        # Get markdown for text extraction
        json_data_markdown = {
            "limit": 1,
            "readability": True,
            "url": url,
            "return_format": "markdown"
        }

        try:
            # Make API requests
            html_response = requests.post(
                'https://api.spider.cloud/crawl',
                headers=headers,
                json=json_data_html
            )

            markdown_response = requests.post(
                'https://api.spider.cloud/crawl',
                headers=headers,
                json=json_data_markdown
            )

            if html_response.status_code != 200 or markdown_response.status_code != 200:
                return f"Error: Could not fetch content. HTML status: {html_response.status_code}, Markdown status: {markdown_response.status_code}"

            # Check if responses contain data
            html_data = html_response.json()
            markdown_data = markdown_response.json()

            if not html_data or not markdown_data or len(html_data) == 0 or len(markdown_data) == 0:
                return f"Error: API returned empty response. URL may be invalid or blocked."

            html_content = html_data[0].get('content', '')
            markdown_content = markdown_data[0].get('content', '')

            if not html_content or not markdown_content:
                return f"Error: API returned empty content. URL may be invalid or blocked."

            # Parse HTML with BeautifulSoup
            from bs4 import BeautifulSoup, NavigableString
            soup = BeautifulSoup(html_content, 'html.parser')

            # Use our enhanced extraction function
            trend_content = self.extract_trend_section_with_images(soup, markdown_content, trend_name, url)

            # Format the output as JSON as required by the task
            output_json = {
                "trend_title": trend_content["trend_title"],
                "description": trend_content["description"],
                "image_url": trend_content["selected_image"],
                "source_url": url
            }

            return json.dumps(output_json, ensure_ascii=False)

        except Exception as e:
            return f"Error: An unexpected error occurred: {str(e)}"

    def extract_trend_section_with_images(self, soup, markdown_content, trend_name, url, chars_before=200,
                                          chars_after=1000):
        """
        Extract the trend section with images embedded, looking deeper for images after description
        """
        # First use markdown to find the trend section
        lines = markdown_content.split('\n')
        heading_pattern = re.compile(r'^(#+)\s+(.*?)$')

        # Find the trend in the markdown content
        found_line_index = -1
        is_heading = False

        # Look for headings first
        for i, line in enumerate(lines):
            match = heading_pattern.match(line)
            if match and trend_name.lower() in match.group(2).lower():
                found_line_index = i
                is_heading = True
                break

        # If not found in headings, search in text
        if found_line_index == -1:
            for i, line in enumerate(lines):
                if trend_name.lower() in line.lower():
                    found_line_index = i
                    break

        # If trend not found
        if found_line_index == -1:
            return {
                "trend_title": trend_name,
                "description": f"Could not find trend '{trend_name}' in the article.",
                "selected_image": "No image found"
            }

        # Extract text content from markdown
        result_lines = []

        # Add context before the trend
        context_before_lines = []
        chars_count = 0

        for j in range(found_line_index - 1, max(0, found_line_index - 10), -1):
            line = lines[j]
            context_before_lines.insert(0, line)
            chars_count += len(line)
            if chars_count >= chars_before:
                break

        result_lines.extend(context_before_lines)

        # Add the trend line
        result_lines.append(lines[found_line_index])

        # Add content after the trend
        context_after_lines = []
        chars_count = 0

        if is_heading:
            heading_level = len(heading_pattern.match(lines[found_line_index]).group(1))
            i = found_line_index + 1

            while i < len(lines) and chars_count < chars_after:
                line = lines[i]
                heading_match = heading_pattern.match(line)

                # Stop at next heading of same/higher level
                if heading_match and len(heading_match.group(1)) <= heading_level:
                    break

                context_after_lines.append(line)
                chars_count += len(line)
                i += 1
        else:
            # Not a heading, just extract characters
            i = found_line_index + 1
            while i < len(lines) and chars_count < chars_after:
                if i < len(lines):  # Ensure we don't access beyond list bounds
                    line = lines[i]
                    context_after_lines.append(line)
                    chars_count += len(line)
                i += 1

        result_lines.extend(context_after_lines)

        # Extract the exact trend title - use the heading if possible
        trend_title = trend_name
        if is_heading:
            match = heading_pattern.match(lines[found_line_index])
            if match:
                trend_title = match.group(2).strip()

        # Combine the markdown content
        markdown_section = '\n'.join(result_lines)

        # Now find this section in the HTML to locate images
        # First, find the trend in HTML
        trend_heading = None
        for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            if trend_name.lower() in heading.text.lower():
                trend_heading = heading
                break

        # If heading not found, look for any element containing the trend name
        if not trend_heading:
            for elem in soup.find_all(['p', 'div', 'span']):
                if trend_name.lower() in elem.text.lower():
                    trend_heading = elem
                    break

        # Create a list to store found images
        found_images = []

        # If we found the trend in HTML, extract its context
        if trend_heading:
            # Get image before trend
            image_before = None
            current = trend_heading.previous_sibling
            while current and not image_before:
                if current.name == 'img' and 'src' in current.attrs:
                    image_before = current['src']
                elif hasattr(current, 'find_all'):
                    imgs = current.find_all('img', src=True)
                    if imgs:
                        # Take the last image (closest to our heading)
                        image_before = imgs[-1]['src']

                current = current.previous_sibling

            if image_before:
                found_images.append(("before", image_before))

            # Get images after trend - look deeper through siblings and children
            image_after = None
            current = trend_heading.next_sibling
            sibling_count = 0
            max_siblings_to_check = 7  # Look deeper in the document

            while current and not image_after and sibling_count < max_siblings_to_check:
                # Check if current element is an image
                if current.name == 'img' and 'src' in current.attrs:
                    image_after = current['src']
                elif hasattr(current, 'find_all'):
                    # Look for images inside this element
                    imgs = current.find_all('img', src=True)
                    if imgs:
                        # Take the first image
                        image_after = imgs[0]['src']

                    # If no direct images but this is a paragraph, look at the next element
                    if not image_after and current.name in ['p', 'div', 'span'] and len(current.get_text().strip()) > 0:
                        # This might be the description paragraph, check the next element
                        next_after_desc = current.next_sibling
                        img_check_count = 0
                        while next_after_desc and img_check_count < 3:  # Check up to 3 elements after description
                            if next_after_desc.name == 'img' and 'src' in next_after_desc.attrs:
                                image_after = next_after_desc['src']
                                break
                            elif hasattr(next_after_desc, 'find_all'):
                                imgs = next_after_desc.find_all('img', src=True)
                                if imgs:
                                    image_after = imgs[0]['src']
                                    break
                            next_after_desc = next_after_desc.next_sibling
                            img_check_count += 1

                current = current.next_sibling
                sibling_count += 1

                # Stop after finding the first image
                if image_after:
                    break

            # If still no image found, try looking at parent's siblings
            if not image_after and trend_heading.parent:
                parent = trend_heading.parent
                next_parent_sibling = parent.next_sibling
                sibling_count = 0

                while next_parent_sibling and not image_after and sibling_count < 3:
                    if next_parent_sibling.name == 'img' and 'src' in next_parent_sibling.attrs:
                        image_after = next_parent_sibling['src']
                    elif hasattr(next_parent_sibling, 'find_all'):
                        imgs = next_parent_sibling.find_all('img', src=True)
                        if imgs:
                            image_after = imgs[0]['src']

                    next_parent_sibling = next_parent_sibling.next_sibling
                    sibling_count += 1

            if image_after:
                found_images.append(("after", image_after))

        # Select the best image based on site-specific rules
        selected_image = None

        # Extract domain from URL to apply site-specific rules
        domain_match = re.search(r'https?://(?:www\.)?([^/]+)', url)
        domain = domain_match.group(1) if domain_match else ""

        if domain.endswith('nashvillelifestyles.com'):
            # For Nashville Lifestyles, prefer image before the trend
            before_images = [img for pos, img in found_images if pos == "before"]
            if before_images:
                selected_image = before_images[0]
        elif domain.endswith('vogue.com'):
            # For Vogue, prefer PNG images
            png_images = [img for _, img in found_images if img.lower().endswith('.png')]
            if png_images:
                selected_image = png_images[0]
        else:
            # For other sites, prefer after images
            after_images = [img for pos, img in found_images if pos == "after"]
            if after_images:
                selected_image = after_images[0]
            elif found_images:  # Fallback to any image if no after images
                selected_image = found_images[0][1]

        # Fallback if no images found with site-specific rules
        if not selected_image and found_images:
            selected_image = found_images[0][1]

        # Extract description
        description = '\n'.join(context_after_lines)

        # Return structured data
        return {
            "trend_title": trend_title,
            "description": description,
            "selected_image": selected_image if selected_image else "No suitable image found"
        }

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
        blocklist_path = 'fashion_trends/config/blocked_urls.json'
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
search_tool = SerperDevTool(n_results=30)
scrape_tool = ScrapeWebsiteTool(text_content=True)
db_tool = TrendDatabaseTool()
blocklist_tool = BlocklistTool()
crawler_tool = UltraMinimalCrawlerTool()