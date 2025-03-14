import requests
import os
import re
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Spider API key from environment variables
SPIDER_API_KEY = os.getenv("SPIDER_API_KEY")

if not SPIDER_API_KEY:
    raise ValueError("SPIDER_API_KEY environment variable is missing. Please add it to your .env file.")


def extract_targeted_fashion_images(html_content, trend_name):
    """
    Specialized method to extract images from fashion websites.
    Focuses on finding images that are most likely related to a specific trend.
    """
    # Parse HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    print(f"Looking for images related to trend: {trend_name}")

    # STRATEGY 1: Find trend heading and look for nearby images
    trend_heading = None
    for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        if trend_name.lower() in heading.text.lower():
            trend_heading = heading
            print(f"Found trend heading: {heading.text.strip()}")
            break

    # If we found the heading, look for images nearby
    trend_images = []
    if trend_heading:
        print("Looking for images near the trend heading...")

        # Look at previous siblings (images often come before headings)
        current = trend_heading.previous_sibling
        count = 0
        while current and count < 5:  # Check up to 5 previous elements
            if current.name == 'img':
                src = current.get('src')
                if src and src.startswith('http'):
                    print(f"Found image before heading: {src}")
                    trend_images.append(src)
            elif hasattr(current, 'find_all'):
                for img in current.find_all('img', src=True):
                    if img['src'].startswith('http'):
                        print(f"Found image in element before heading: {img['src']}")
                        trend_images.append(img['src'])
            count += 1
            current = current.previous_sibling

        # Look at parent and its previous siblings (for nested structures)
        parent = trend_heading.parent
        if parent:
            current = parent.previous_sibling
            count = 0
            while current and count < 3:  # Check up to 3 previous elements
                if hasattr(current, 'find_all'):
                    for img in current.find_all('img', src=True):
                        if img['src'].startswith('http'):
                            print(f"Found image in parent's previous sibling: {img['src']}")
                            trend_images.append(img['src'])
                count += 1
                current = current.previous_sibling

    # If we found trend-specific images, return them right away
    if trend_images:
        print(f"STRATEGY 1 SUCCESS: Found {len(trend_images)} trend-specific images")
        return trend_images[:3]  # Return up to 3 trend-specific images

    # STRATEGY 2: If no trend-specific images found, look for runway/collection images
    print("No trend-specific images found. Looking for runway/collection images...")
    runway_images = []

    # Look for figure or div elements that might contain runway images
    for fig in soup.find_all(['figure', 'div']):
        # Check if this element has text mentioning runways or collections
        if fig.text and any(term in fig.text.lower() for term in ['runway', 'collection', 'spring 2025']):
            for img in fig.find_all('img', src=True):
                if img['src'].startswith('http'):
                    print(f"Found runway image: {img['src']}")
                    runway_images.append(img['src'])

    # Also look for image attributes with runway keywords
    for img in soup.find_all('img'):
        src = img.get('src', '')
        alt = img.get('alt', '')
        if src.startswith('http') and any(
                term in (src.lower() + alt.lower()) for term in ['runway', 'collection', 'spring', '2025']):
            print(f"Found image with runway keywords: {src}")
            runway_images.append(src)

    if runway_images:
        print(f"STRATEGY 2 SUCCESS: Found {len(runway_images)} runway images")
        return runway_images[:3]  # Return up to 3 runway images

    # STRATEGY 3: Last resort - try to find any fashion images on the page
    print("No runway images found. Looking for any fashion images...")
    fashion_images = []
    for img in soup.find_all('img'):
        src = img.get('src')
        if not src or not src.startswith('http'):
            continue

        # Skip small images, icons, etc.
        if 'icon' in src.lower() or 'logo' in src.lower():
            continue

        # Look for indicators that this is a fashion/clothing image
        alt = img.get('alt', '').lower()
        if any(term in alt for term in ['wear', 'dress', 'fashion', 'outfit', 'look', 'trend', 'style']):
            print(f"Found fashion image (from alt text): {src}")
            fashion_images.append(src)

        # Also check if the image URL suggests it's a main content image
        if any(term in src.lower() for term in ['jpg', 'jpeg', 'png']) and not any(
                term in src.lower() for term in ['icon', 'logo', 'avatar']):
            if src not in fashion_images:  # Avoid duplicates
                print(f"Found potential fashion image: {src}")
                fashion_images.append(src)

    print(f"STRATEGY 3 RESULT: Found {len(fashion_images)} general fashion images")
    return fashion_images[:3]  # Return up to 3 general fashion images


def extract_trend_section(full_content, trend_name, chars_to_extract=1000):
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

    # Add context from lines before the found line (up to 100 chars worth)
    if found_line_index > 0:
        chars_before = 0
        context_lines = []

        # Go backward from the found line until we have about 100 chars
        for j in range(found_line_index - 1, max(0, found_line_index - 5), -1):
            line = lines[j]
            context_lines.insert(0, line)  # Insert at beginning to maintain order
            chars_before += len(line)

            if chars_before >= 100:
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


def image_extraction(url, trend_name):
    """
    Test improved image extraction for a specific fashion article and trend.
    """
    headers = {
        'Authorization': f'Bearer {SPIDER_API_KEY}',
        'Content-Type': 'application/json'
    }

    # Get HTML content
    json_data_html = {
        "limit": 1,
        "readability": False,  # Use False for raw HTML to capture all elements
        "url": url,
        "return_format": "html"
    }

    # Also get markdown for text extraction
    json_data_markdown = {
        "limit": 1,
        "readability": True,
        "url": url,
        "return_format": "markdown"
    }

    # Get raw HTML first
    print(f"Fetching HTML content from {url}...")
    html_response = requests.post(
        'https://api.spider.cloud/crawl',
        headers=headers,
        json=json_data_html
    )

    # Get markdown for text content
    print(f"Fetching Markdown content from {url}...")
    markdown_response = requests.post(
        'https://api.spider.cloud/crawl',
        headers=headers,
        json=json_data_markdown
    )

    html_content = ""
    markdown_content = ""

    if html_response.status_code == 200:
        html_result = html_response.json()
        if html_result and len(html_result) > 0:
            html_content = html_result[0]['content']
            print(f"HTML content successfully retrieved ({len(html_content)} characters)")
    else:
        print(f"Error fetching HTML: {html_response.status_code}")

    if markdown_response.status_code == 200:
        markdown_result = markdown_response.json()
        if markdown_result and len(markdown_result) > 0:
            markdown_content = markdown_result[0]['content']
            print(f"Markdown content successfully retrieved ({len(markdown_content)} characters)")
    else:
        print(f"Error fetching Markdown: {markdown_response.status_code}")

    # Extract trend section from markdown for text content
    print(f"\nExtracting trend section for '{trend_name}'...")
    trend_section = ""
    if markdown_content:
        trend_section = extract_trend_section(markdown_content, trend_name, 800)
        print(f"Trend section extracted ({len(trend_section)} characters)")
        print("\nTREND SECTION EXCERPT:")
        print(trend_section[:300] + "...")

    # Extract image URLs using our targeted approach
    print(f"\nExtracting images related to '{trend_name}' using targeted approach...")
    image_urls = extract_targeted_fashion_images(html_content, trend_name)

    print(f"\nFINAL TARGETED IMAGES ({len(image_urls)}):")
    for i, img_url in enumerate(image_urls):
        print(f"{i + 1}. {img_url}")

    return image_urls


# Main execution
if __name__ == "__main__":
    # You can change these values to test different websites and trends
    website_url = "https://www.vogue.com/article/spring-2025-fashion-trends"
    trend_to_find = "Summertime Prep"

    print(f"Testing targeted image extraction for trend '{trend_to_find}' on {website_url}\n")
    images = image_extraction(website_url, trend_to_find)