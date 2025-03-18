import os
import re
import requests
from bs4 import BeautifulSoup, NavigableString
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()
SPIDER_API_KEY = os.getenv("SPIDER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def get_caption_for_element(element):
    """Find caption text for an element by checking various common patterns"""
    caption = None

    # 1. Check for next sibling that might be a caption
    next_elem = element.next_sibling
    while next_elem and not caption:
        if isinstance(next_elem, NavigableString):
            next_elem = next_elem.next_sibling
            continue

        if next_elem.name in ['figcaption', 'small', 'em', 'i', 'span', 'p', 'div'] and next_elem.text.strip():
            caption_text = next_elem.text.strip()
            # Look for brand name patterns in captions
            brand_patterns = [
                r'(?:from left|from right|runway|image credit)[:;]?\s+(.+)',
                r'(.+?)(?:\s+\/\s+.+)+',  # Brand / Brand / Brand pattern
                r'^\s*\d+\.\s*(.+?)(?:\s+\/\s+.+|\s+\d+\.\s*.+)*$'  # 1. Brand / 2. Brand pattern
            ]

            for pattern in brand_patterns:
                match = re.search(pattern, caption_text, re.IGNORECASE)
                if match:
                    caption = caption_text
                    break

            if not caption and (
                    re.search(
                        r'chanel|prada|miu\s?miu|vogue|giambattista|ralph lauren|burberry|gucci|versace|louis vuitton',
                        caption_text, re.IGNORECASE)
            ):
                caption = caption_text

            if not caption and len(caption_text) < 100:  # Short text is likely a caption
                caption = caption_text

        next_elem = next_elem.next_sibling

    # 2. Check for figure with figcaption
    if not caption:
        parent_fig = element.find_parent('figure')
        if parent_fig:
            figcaption = parent_fig.find('figcaption')
            if figcaption and figcaption.text.strip():
                caption = figcaption.text.strip()

    # 3. Check for nearby small text or italics
    if not caption:
        parent = element.parent
        if parent:
            small_text = parent.find_all(['small', 'em', 'i'], limit=2)
            for text in small_text:
                if text.text.strip() and len(text.text.strip()) < 100:
                    caption = text.text.strip()
                    break

    # 4. Look for attribute with caption information
    if not caption:
        for attr in ['alt', 'title', 'data-caption']:
            if attr in element.attrs and element[attr].strip():
                caption = element[attr].strip()
                break

    # 5. Check for caption inside noscript (common in lazy-loaded images)
    if not caption and element.find_parent('noscript'):
        next_elem = element.find_parent('noscript').next_sibling
        if next_elem and hasattr(next_elem, 'text') and next_elem.text.strip():
            short_text = next_elem.text.strip()
            if len(short_text) < 100:
                caption = short_text

    return caption


def get_image_with_caption(element):
    """Extract an image URL"""
    if element.name == 'img' and 'src' in element.attrs:
        return f"IMAGE URL: {element['src']}"
    return None


def extract_trend_section_with_images(soup, markdown_content, trend_name, chars_before=200, chars_after=1000):
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
        return f"Could not find trend '{trend_name}' in the article."

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

    # If we found the trend in HTML, extract its context
    if trend_heading:
        # Get one image before trend (closest to the heading)
        image_before = None
        current = trend_heading.previous_sibling
        while current and not image_before:
            if current.name == 'img' and 'src' in current.attrs:
                image_before = f"IMAGE URL: {current['src']}"
            elif hasattr(current, 'find_all'):
                imgs = current.find_all('img', src=True)
                if imgs:
                    # Take the last image (closest to our heading)
                    image_before = f"IMAGE URL: {imgs[-1]['src']}"

            current = current.previous_sibling

        # If we found an image before the trend, insert it
        if image_before:
            lines = markdown_section.split('\n')
            # Find the trend heading line
            for i, line in enumerate(lines):
                if trend_name.lower() in line.lower():
                    # Insert just one image before this line
                    lines.insert(i, image_before)
                    break
            markdown_section = '\n'.join(lines)

        # Get images after trend - look deeper through siblings and children
        image_after = None
        current = trend_heading.next_sibling
        sibling_count = 0
        max_siblings_to_check = 7  # Increase this to look deeper in the document

        while current and not image_after and sibling_count < max_siblings_to_check:
            # Check if current element is an image
            if current.name == 'img' and 'src' in current.attrs:
                image_after = f"IMAGE URL: {current['src']}"
            elif hasattr(current, 'find_all'):
                # Look for images inside this element
                imgs = current.find_all('img', src=True)
                if imgs:
                    # Take the first image
                    image_after = f"IMAGE URL: {imgs[0]['src']}"

                # If no direct images but this is a paragraph, look at the next element
                if not image_after and current.name in ['p', 'div', 'span'] and len(current.get_text().strip()) > 0:
                    # This might be the description paragraph, check the next element
                    next_after_desc = current.next_sibling
                    img_check_count = 0
                    while next_after_desc and img_check_count < 3:  # Check up to 3 elements after description
                        if next_after_desc.name == 'img' and 'src' in next_after_desc.attrs:
                            image_after = f"IMAGE URL: {next_after_desc['src']}"
                            break
                        elif hasattr(next_after_desc, 'find_all'):
                            imgs = next_after_desc.find_all('img', src=True)
                            if imgs:
                                image_after = f"IMAGE URL: {imgs[0]['src']}"
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
                    image_after = f"IMAGE URL: {next_parent_sibling['src']}"
                elif hasattr(next_parent_sibling, 'find_all'):
                    imgs = next_parent_sibling.find_all('img', src=True)
                    if imgs:
                        image_after = f"IMAGE URL: {imgs[0]['src']}"

                next_parent_sibling = next_parent_sibling.next_sibling
                sibling_count += 1

        # If we found an image after the trend, insert it
        if image_after:
            lines = markdown_section.split('\n')
            for j, line in enumerate(lines):
                if trend_name.lower() in line.lower():
                    # Insert image after this line
                    lines.insert(j + 1, image_after)
                    break
            markdown_section = '\n'.join(lines)

        # Look for just one data-src attribute (closest to the trend)
        data_src_image = None

        # Check nearby elements for data-src attributes
        for elem in soup.find_all():
            if trend_name.lower() in elem.text.lower() or (
                    elem.parent and trend_name.lower() in elem.parent.text.lower()):
                # Look for data-src in this element and surrounding elements
                for attr in elem.attrs:
                    if attr.startswith('data-') and 'src' in attr and isinstance(elem[attr], str) and (
                            elem[attr].endswith('.jpg') or elem[attr].endswith('.png')):
                        data_src_image = f"DATA-SRC IMAGE URL: {elem[attr]}"
                        break

                # Check parent and siblings if we haven't found an image yet
                if not data_src_image and elem.parent:
                    for sibling in list(elem.parent.children):
                        for attr in getattr(sibling, 'attrs', {}):
                            if attr.startswith('data-') and 'src' in attr and isinstance(sibling[attr], str) and (
                                    sibling[attr].endswith('.jpg') or sibling[attr].endswith('.png')):
                                data_src_image = f"DATA-SRC IMAGE URL: {sibling[attr]}"
                                break
                        if data_src_image:
                            break

            if data_src_image:
                break

        # Add data-src image if found
        if data_src_image:
            lines = markdown_section.split('\n')
            for i, line in enumerate(lines):
                if trend_name.lower() in line.lower():
                    # Insert after the trend heading and any previously inserted image
                    insert_pos = i + 1
                    while insert_pos < len(lines) and lines[insert_pos].startswith(
                            ("IMAGE URL:", "DATA-SRC IMAGE URL:")):
                        insert_pos += 1

                    lines.insert(insert_pos, data_src_image)
                    break

            markdown_section = '\n'.join(lines)

    return markdown_section


def extract_trend_with_inline_images(url, trend_name):
    """
    Extract trend content with images embedded inline at their proper positions.

    Args:
        url: The article URL
        trend_name: The trend name to extract

    Returns:
        A string with the trend content and inline image URLs
    """
    # API request headers
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
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find and extract the trend section with images
        return extract_trend_section_with_images(soup, markdown_content, trend_name)

    except IndexError as e:
        return f"Error: Failed to process API response: {str(e)}. This usually happens when the API returns an unexpected format."
    except Exception as e:
        return f"Error: An unexpected error occurred: {str(e)}"


# Create the tool schema
class ExtractTrendInfoSchema(BaseModel):
    url: str = Field(..., description="The URL of the fashion article")
    trend_name: str = Field(..., description="The name of the trend to extract")


# Create the tool
class ExtractTrendInfoTool(BaseTool):
    name: str = "Extract Trend Info"
    description: str = "Extract trend information including name, description, and images from a fashion website."
    args_schema: type[BaseModel] = ExtractTrendInfoSchema

    def _run(self, url: str, trend_name: str) -> str:
        return extract_trend_with_inline_images(url, trend_name)


# Create an agent that will analyze the extracted information
def create_analyzer_agent():
    return Agent(
        role="Fashion Trend Analyzer",
        goal="Analyze fashion trend information and identify key elements",
        backstory="""You are a fashion expert with a keen eye for trends and styles.
        Your specialty is analyzing fashion content and extracting the most relevant information
        including exact trend names, descriptions, and identifying images that show people wearing 
        the trend (not just product images).""",
        verbose=True,
        tools=[ExtractTrendInfoTool()],
        llm="openai/gpt-4o-mini-2024-07-18"  # Using the specified model
    )


# Create a task with specific URLs
def create_specific_analysis_task(url, trend_name):
    return Task(
        description=f"""
        Analyze the fashion trend information from the URL: "{url}" for the trend "{trend_name}".
        DO NOT modify the URL - use exactly the URL provided.
        
        From the extracted content, provide the following:
        1. The EXACT trend title as it appears in the article
        2. The description of the trend, formatted nicely but using the EXACT text from the article
        3. Select the most relevant image URL that shows people/models wearing the trend (avoid product-only images)
        
        For the image selection:
        - Important: Different fashion sites place images in different locations:
          * For nashvillelifestyles, always choose the image that appears before the trend title
          * For Vogue, always choose .png images when available
          * For InStyle, look for images that appear after the trend description (not just after the title)
          * For other sites, examine all available images
        - Pay attention to any text that follows the IMAGE URL in the extracted content - this often contains descriptions
          like "From left: Brand X, Brand Y, Brand Z" or "Runway: Designer Spring 2025" which indicates runway/model images
        - Show real people or models wearing the trend (not product-only images)
        - Prioritize images that show fashion runway models or editorial photoshoots
        
        Format your response as:
        TREND TITLE: [exact title]
        DESCRIPTION: [formatted description]
        SELECTED IMAGE URL: [url]
        """,
        expected_output="A structured analysis of the trend with title, description, and selected image URL",
    )


# Main function to run the test
if __name__ == "__main__":
    # Define our examples
    examples = [
        {
            "url": "https://www.cosmopolitan.com/uk/fashion/style/a63238403/fashion-trends-2025/",
            "trend": "Soft Ballet Pink"
        },
        {
            "url": "https://www.instyle.de/mode/modetrends",
            "trend": "Modetrend 2025: Athleisure"
        }
    ]

    # Create the agent
    analyzer_agent = create_analyzer_agent()

    # Run each example individually
    for example in examples:
        print(f"\n\n===== ANALYZING TREND: {example['trend']} FROM {example['url']} =====\n")

        # Create a task with the exact URL and trend
        analysis_task = create_specific_analysis_task(example['url'], example['trend'])
        analysis_task.agent = analyzer_agent

        # Create a crew with just this agent and task
        crew = Crew(
            agents=[analyzer_agent],
            tasks=[analysis_task],
            verbose=True
        )

        # Run the crew and get the result
        result = crew.kickoff()

        print("\n========== ANALYSIS RESULT ==========")
        print(result)
        print("====================================")