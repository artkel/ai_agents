#!/usr/bin/env python3
"""
Fiverr Markdown Cleaner

This script cleans up a markdown file containing Fiverr content by:
1. Removing navigation menu content
2. Removing footer content
3. Removing "Recommended for you" sections
4. Removing content between "###### General" and "BasicStandardPremium"
5. Removing standalone markdown links
6. Cleaning up excessive whitespace

Usage:
    python fiverr_md_cleaner.py

The script expects a file named 'fiverr_profiles_raw.md' in the 'output' directory
and will save the cleaned version as 'fiverr_profiles_clean.md' in the same directory.
"""

import re
import os


def clean_markdown_file(input_path, output_path):
    """
    Clean up a markdown file by removing specific patterns.

    Args:
        input_path (str): Path to the input markdown file
        output_path (str): Path to save the cleaned markdown file
    """
    # Read the input file
    try:
        with open(input_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception as e:
        print(f"Error reading file {input_path}: {e}")
        return False

    # Pattern 1: Remove the first block (Navigation links)
    navigation_pattern = r'\[\]\(https://www\.fiverr\.com/\?source=top_nav\)[\s\S]*?I want to offer Pro services'
    content = re.sub(navigation_pattern, '', content)

    # Pattern 2: Remove footer content (from the pasted example)
    footer_pattern = r'###### Categories[\s\S]*?© Fiverr International Ltd\. 2025[\s\S]*?Fiverr on Twitter'
    content = re.sub(footer_pattern, '', content)

    # Pattern 3: Remove content between "#### Recommended for you" and the next "##" heading
    # The pattern matches up to the next heading or end of file if no heading exists
    recommended_pattern = r'#### Recommended for you[\s\S]*?(?=\n## |$)'
    content = re.sub(recommended_pattern, '', content)

    # Pattern 4: Remove content between "###### General" and "BasicStandardPremium"
    # But keep both of these markers
    currency_pattern = r'(###### General\n)[\s\S]*?(?=BasicStandardPremium)'
    content = re.sub(currency_pattern, r'\1', content)

    # Pattern 5: Remove lines that only contain markdown links [text](https...)
    link_pattern = r'^\s*\[.*?\]\(https?://.*?\)\s*$'
    filtered_lines = []

    for line in content.split('\n'):
        if not re.match(link_pattern, line.strip()):
            filtered_lines.append(line)

    content = '\n'.join(filtered_lines)

    # Remove consecutive empty lines
    content = re.sub(r'\n{3,}', '\n\n', content)

    # Write the cleaned content to the output file
    try:
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Successfully cleaned the markdown file. Saved to {output_path}")
        return True
    except Exception as e:
        print(f"Error writing to file {output_path}: {e}")
        return False


if __name__ == "__main__":
    # Define input and output paths
    input_file = "fiverr_profiles_raw.md"
    output_file = "fiverr_profiles_clean.md"

    # Get the current directory
    current_dir = os.getcwd()

    # Define full paths
    input_path = os.path.join(current_dir, "output", input_file)
    output_path = os.path.join(current_dir, "output", output_file)

    # Clean the markdown file
    success = clean_markdown_file(input_path, output_path)

    if success:
        print(f"Original file: {input_path}")
        print(f"Cleaned file: {output_path}")

        # Get file sizes to show the difference
        original_size = os.path.getsize(input_path)
        cleaned_size = os.path.getsize(output_path)
        size_diff = original_size - cleaned_size
        percent_reduced = (size_diff / original_size) * 100

        print(f"Original size: {original_size:,} bytes")
        print(f"Cleaned size: {cleaned_size:,} bytes")
        print(f"Reduced by: {size_diff:,} bytes ({percent_reduced:.2f}%)")
    else:
        print("Failed to clean the markdown file.")