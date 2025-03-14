import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Spider API key from environment variables
SPIDER_API_KEY = os.getenv("SPIDER_API_KEY")

if not SPIDER_API_KEY:
    raise ValueError("SPIDER_API_KEY environment variable is missing. Please add it to your .env file.")

headers = {
    'Authorization': f'Bearer {SPIDER_API_KEY}',
    'Content-Type': 'application/json'}

url = "https://www.vogue.com/article/spring-2025-fashion-trends"
trend_name = "Summertime Prep"

json_data = {
    "limit": 1,
    "readability": False,
    "url": url,
    "return_format": "markdown"
}

# Print request information for debugging
print(f"Making request to Spider API with key: {SPIDER_API_KEY[:5]}...")
print(f"Request URL: https://api.spider.cloud/crawl")
print(f"Request data: {json_data}")

response = requests.post('https://api.spider.cloud/crawl',
                    headers=headers,
                    json=json_data)

# Print response information for debugging
print(f"Response status code: {response.status_code}")
print(f"Response headers: {response.headers}")
print(f"Response content (first 500 chars): {response.text[:500]}")

# Only try to parse JSON if the status code indicates success
if response.status_code == 200:
    try:
        json_data = response.json()
        print("Successfully parsed JSON response")
        print(json_data)
    except Exception as e:
        print(f"Error parsing JSON: {e}")
else:
    print("Request failed with non-200 status code")

# def extract_trend_section(full_content, trend_name, chars_to_extract=1000):
#     """
#     Extract a section around a trend name, focusing on actual headings.
#     Also includes context before the heading when possible.
#     """
#     import re
#
#     # Split the content into lines
#     lines = full_content.split('\n')
#
#     # Look for the trend name in markdown headings (# Heading)
#     heading_pattern = re.compile(r'^(#+)\s+(.*?)$')
#
#     found_line_index = -1
#     is_heading = False
#
#     # First, try to find the trend name in a markdown heading
#     for i, line in enumerate(lines):
#         match = heading_pattern.match(line)
#         if match and trend_name.lower() in match.group(2).lower():
#             found_line_index = i
#             is_heading = True
#             break
#
#     # If not found in headings, look for the trend name anywhere
#     if found_line_index == -1:
#         for i, line in enumerate(lines):
#             if trend_name.lower() in line.lower():
#                 found_line_index = i
#                 break
#
#     # If still not found, return an error
#     if found_line_index == -1:
#         return f"Error: Could not find trend '{trend_name}' in the article."
#
#     # Now extract the content - including context before the heading when possible
#     result = []
#
#     # Add context from lines before the found line (up to 30 chars worth)
#     if found_line_index > 0:
#         chars_before = 0
#         context_lines = []
#
#         # Go backward from the found line until we have about 30 chars
#         for j in range(found_line_index - 1, max(0, found_line_index - 5), -1):
#             line = lines[j]
#             context_lines.insert(0, line)  # Insert at beginning to maintain order
#             chars_before += len(line)
#
#             if chars_before >= 100:
#                 break
#
#         # Add the context lines to the result
#         result.extend(context_lines)
#
#     # Add the found line
#     result.append(lines[found_line_index])
#
#     # If it's a heading, extract content until the next heading of same or higher level
#     if is_heading:
#         heading_level = len(heading_pattern.match(lines[found_line_index]).group(1))
#
#         chars_count = len(lines[found_line_index])
#         i = found_line_index + 1
#
#         while i < len(lines) and chars_count < chars_to_extract:
#             line = lines[i]
#             heading_match = heading_pattern.match(line)
#
#             # Stop if we hit another heading of same or higher level
#             if heading_match and len(heading_match.group(1)) <= heading_level:
#                 break
#
#             result.append(line)
#             chars_count += len(line)
#             i += 1
#     else:
#         # Not a heading, just extract a certain number of characters
#         chars_count = len(lines[found_line_index])
#         i = found_line_index + 1
#
#         while i < len(lines) and chars_count < chars_to_extract:
#             result.append(lines[i])
#             chars_count += len(lines[i])
#             i += 1
#
#     # Join the lines back together
#     return '\n'.join(result)
#
# full_content = response.json()[0]['content'].rstrip()
# trend_section = extract_trend_section(full_content, trend_name, 1000)
# print(trend_section)



# print("##########################")
# print(response.json()[0]['content'].rstrip())
# print("##########################")
# print(len(response.json()[0]['content'].rstrip()))

# full_content = response.json()[0]['content'].rstrip()
# print(full_content.find("Yellow Yellow Yellow"))

# full_content = response.json()[0]['content'].rstrip()
# trend_name = "###"
# trend_index = full_content.find(trend_name)

# if trend_index >= 0:
#     # Extract exactly 1000 characters after the trend name
#     chars_after_trend = 1000
#
#     # Include the trend name itself, some context before it, and chars_after_trend characters after it
#     context_before = 1  # Characters before the trend name for context
#     section_start = max(0, trend_index - context_before)
#     section_end = 1000 + section_start
#
#     trend_section = full_content[section_start:section_end]
#
#     print(trend_section)
# else:
#     print(f"Error: Could not find trend '{trend_name}' in the article. Please check the spelling.")


#print(response.json()[0]['content'])
