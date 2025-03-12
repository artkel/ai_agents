#!/usr/bin/env python3
"""
CrewAI Markdown Documentation Cleaner

This script cleans up markdown documentation by removing navigation elements,
logos, search bars, and other UI elements typically found in web documentation
but not needed in pure markdown files.
"""

import os
import re
import argparse
from pathlib import Path


def load_unwanted_content(file_path=None):
    """
    Load unwanted content patterns from the specified file or use default patterns.

    Args:
        file_path: Path to a file containing unwanted content

    Returns:
        A list of patterns to remove
    """
    # If a specific file is provided, load its content as unwanted patterns
    if file_path and os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            # Create a more effective pattern by splitting into individual sections
            # This helps when dealing with large chunks of text
            patterns = []
            # Add the entire content as one pattern
            patterns.append(content)
            # Also add navigation sections separately for more targeted removal
            nav_sections = re.findall(r'#{1,6}\s+([^\n]+)[\s\S]*?(?=#{1,6}\s+|$)', content)
            for section in nav_sections:
                if section:
                    patterns.append(f"#{{{1, 6}}}\\s+{re.escape(section)}[\\s\\S]*?(?=#{{{1, 6}}}\\s+|$)")

            return patterns

    # Default unwanted patterns if no file is provided or file doesn't exist
    return [
        r'Search\.\.\.',
        r'Navigation',
        r'\[Get Started\].*?\)',
        r'\[CrewAI home page.*?\)',
        r'\* \[Community\].*?\)',
        r'\* \[Changelog\].*?\)',
        r'##### Get Started[\s\S]*?(?=##### |$)',
        r'##### Core Concepts[\s\S]*?(?=##### |$)',
        r'##### How to Guides[\s\S]*?(?=##### |$)',
        r'##### Tools[\s\S]*?(?=##### |$)',
        r'##### Telemetry[\s\S]*?(?=##### |$)',
        r'!\[.*?\]\(.*?\)',  # Remove image references
        r'\[\s*\]\s*\(\s*https://.*?\)',  # Remove empty links with potential whitespace
        r'\[\s*\]\s*\(\s*https://docs\.crewai\.com.*?\)',  # Specific pattern for CrewAI docs
        r'\[\s*ZWSP\s*\]\s*\(\s*https://.*?\)',  # Remove ZWSP links with potential whitespace
        r'Was this page helpful\?\s*YesNo',  # Remove feedback section
        r'\[website\]\(https://crewai\.com\).*?On this page',  # Remove footer links
        r'\[Powered by Mintlify\].*?',  # Remove powered by section
        r'On this page\s*'
]

def clean_markdown(input_content, unwanted_patterns):
    """
    Clean markdown content by removing unwanted patterns.

    Args:
        input_content: The markdown content to clean
        unwanted_patterns: List of patterns to remove

    Returns:
        Cleaned markdown content
    """
    cleaned_content = input_content

    for pattern in unwanted_patterns:
        # Try exact match first if pattern is not too large
        if len(pattern) < 10000:  # Avoid replacing huge chunks directly
            cleaned_content = cleaned_content.replace(pattern, '')

        # Then try regex pattern matching
        try:
            cleaned_content = re.sub(pattern, '', cleaned_content)
        except re.error:
            # If regex fails, just continue with next pattern
            continue

    # Additional cleaning specific to the CrewAI documentation

    # Remove navigation elements
    cleaned_content = re.sub(r'Navigation.*?\n', '', cleaned_content)
    cleaned_content = re.sub(r'Search\.\.\..*?\n', '', cleaned_content)

    # Remove list items that are likely navigation links
    cleaned_content = re.sub(r'^\s*\*\s+\[.*?\]\(.*?\)\s*$', '', cleaned_content, flags=re.MULTILINE)
    cleaned_content = re.sub(r'^\s*\*\s+\[.*?\].*?$', '', cleaned_content, flags=re.MULTILINE)

    # Remove image references
    cleaned_content = re.sub(r'!\[.*?\]\(.*?\)', '', cleaned_content)

    # Remove empty markdown links (ZWSP links) - with improved pattern matching
    cleaned_content = re.sub(r'\[\s*\]\s*\(\s*https://.*?\)', '', cleaned_content)
    cleaned_content = re.sub(r'\[\s*ZWSP\s*\]\s*\(\s*https://.*?\)', '', cleaned_content)

    # Additional pattern specifically for docs.crewai.com links which might be problematic
    cleaned_content = re.sub(r'\[\s*\]\s*\(\s*https://docs\.crewai\.com.*?\)', '', cleaned_content)

    # Remove "Was this page helpful?" section
    cleaned_content = re.sub(r'Was this page helpful\?\s*YesNo', '', cleaned_content)

    # Remove footer links and powered by section
    footer_pattern = r'\[website\]\(https://crewai\.com\).*?On this page'
    cleaned_content = re.sub(footer_pattern, '', cleaned_content, flags=re.DOTALL)
    cleaned_content = re.sub(r'\[Powered by Mintlify\].*?$', '', cleaned_content, flags=re.MULTILINE)
    cleaned_content = re.sub(r'On this page\s*$', '', cleaned_content, flags=re.MULTILINE)

    # Remove headings with navigation sections
    cleaned_content = re.sub(r'#{1,6}\s+Get Started.*?(?=#{1,6}|$)', '', cleaned_content, flags=re.DOTALL)
    cleaned_content = re.sub(r'#{1,6}\s+Core Concepts.*?(?=#{1,6}|$)', '', cleaned_content, flags=re.DOTALL)
    cleaned_content = re.sub(r'#{1,6}\s+How to Guides.*?(?=#{1,6}|$)', '', cleaned_content, flags=re.DOTALL)
    cleaned_content = re.sub(r'#{1,6}\s+Tools.*?(?=#{1,6}|$)', '', cleaned_content, flags=re.DOTALL)
    cleaned_content = re.sub(r'#{1,6}\s+Telemetry.*?(?=#{1,6}|$)', '', cleaned_content, flags=re.DOTALL)

    # Clean up multiple blank lines
    cleaned_content = re.sub(r'\n{3,}', '\n\n', cleaned_content)

    return cleaned_content.strip()


def main():
    parser = argparse.ArgumentParser(description='Clean up markdown documentation by removing unwanted content.')
    parser.add_argument('--input_file', default='output/crewai_documentation_raw.md',
                        help='Input markdown file to clean (default: output/crewai_documentation_raw.md)')
    parser.add_argument('-o', '--output', default='output/crewai_documentation_clean.md',
                        help='Output file path (default: output/crewai_documentation_clean.md)')
    parser.add_argument('-p', '--patterns', default='output/unwanted_content.txt',
                        help='File containing patterns to remove (default: output/unwanted_content.txt)')

    args = parser.parse_args()

    # Read input file
    try:
        with open(args.input_file, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Error: Input file '{args.input_file}' not found.")
        return

    # Load unwanted content patterns
    unwanted_patterns = load_unwanted_content(args.patterns)

    # Clean the markdown
    cleaned_content = clean_markdown(content, unwanted_patterns)

    # Determine output file path
    output_path = args.output

    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Write cleaned content to output file
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_content)

    print(f"Cleaned markdown saved to {output_path}")


if __name__ == "__main__":
    main()
    # Remove "On this page" text


def clean_markdown(input_content, unwanted_patterns):
    """
    Clean markdown content by removing unwanted patterns.

    Args:
        input_content: The markdown content to clean
        unwanted_patterns: List of patterns to remove

    Returns:
        Cleaned markdown content
    """
    cleaned_content = input_content

    for pattern in unwanted_patterns:
        # Try exact match first if pattern is not too large
        if len(pattern) < 10000:  # Avoid replacing huge chunks directly
            cleaned_content = cleaned_content.replace(pattern, '')

        # Then try regex pattern matching
        try:
            cleaned_content = re.sub(pattern, '', cleaned_content)
        except re.error:
            # If regex fails, just continue with next pattern
            continue

    # Additional cleaning specific to the CrewAI documentation

    # Remove navigation elements
    cleaned_content = re.sub(r'Navigation.*?\n', '', cleaned_content)
    cleaned_content = re.sub(r'Search\.\.\..*?\n', '', cleaned_content)

    # Remove list items that are likely navigation links
    cleaned_content = re.sub(r'^\s*\*\s+\[.*?\]\(.*?\)\s*$', '', cleaned_content, flags=re.MULTILINE)
    cleaned_content = re.sub(r'^\s*\*\s+\[.*?\].*?$', '', cleaned_content, flags=re.MULTILINE)

    # Remove image references
    cleaned_content = re.sub(r'!\[.*?\]\(.*?\)', '', cleaned_content)

    # Remove empty markdown links (ZWSP links) - with improved pattern matching
    cleaned_content = re.sub(r'\[\s*\]\s*\(\s*https://.*?\)', '', cleaned_content)
    cleaned_content = re.sub(r'\[\s*ZWSP\s*\]\s*\(\s*https://.*?\)', '', cleaned_content)

    # Additional pattern specifically for docs.crewai.com links which might be problematic
    cleaned_content = re.sub(r'\[\s*\]\s*\(\s*https://docs\.crewai\.com.*?\)', '', cleaned_content)

    # Remove "Was this page helpful?" section
    cleaned_content = re.sub(r'Was this page helpful\?\s*YesNo', '', cleaned_content)

    # Remove footer links and powered by section
    footer_pattern = r'\[website\]\(https://crewai\.com\).*?On this page'
    cleaned_content = re.sub(footer_pattern, '', cleaned_content, flags=re.DOTALL)
    cleaned_content = re.sub(r'\[Powered by Mintlify\].*?$', '', cleaned_content, flags=re.MULTILINE)
    cleaned_content = re.sub(r'On this page\s*$', '', cleaned_content, flags=re.MULTILINE)

    # Remove headings with navigation sections
    cleaned_content = re.sub(r'#{1,6}\s+Get Started.*?(?=#{1,6}|$)', '', cleaned_content, flags=re.DOTALL)
    cleaned_content = re.sub(r'#{1,6}\s+Core Concepts.*?(?=#{1,6}|$)', '', cleaned_content, flags=re.DOTALL)
    cleaned_content = re.sub(r'#{1,6}\s+How to Guides.*?(?=#{1,6}|$)', '', cleaned_content, flags=re.DOTALL)
    cleaned_content = re.sub(r'#{1,6}\s+Tools.*?(?=#{1,6}|$)', '', cleaned_content, flags=re.DOTALL)
    cleaned_content = re.sub(r'#{1,6}\s+Telemetry.*?(?=#{1,6}|$)', '', cleaned_content, flags=re.DOTALL)

    # Clean up multiple blank lines
    cleaned_content = re.sub(r'\n{3,}', '\n\n', cleaned_content)

    return cleaned_content.strip()


def main():
    parser = argparse.ArgumentParser(description='Clean up markdown documentation by removing unwanted content.')
    parser.add_argument('--input_file', default='output/crewai_documentation_raw.md',
                        help='Input markdown file to clean (default: output/crewai_documentation_raw.md)')
    parser.add_argument('-o', '--output', default='output/crewai_documentation_clean.md',
                        help='Output file path (default: output/crewai_documentation_clean.md)')
    parser.add_argument('-p', '--patterns', default='output/unwanted_content.txt',
                        help='File containing patterns to remove (default: output/unwanted_content.txt)')

    args = parser.parse_args()

    # Read input file
    try:
        with open(args.input_file, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Error: Input file '{args.input_file}' not found.")
        return

    # Load unwanted content patterns
    unwanted_patterns = load_unwanted_content(args.patterns)

    # Clean the markdown
    cleaned_content = clean_markdown(content, unwanted_patterns)

    # Determine output file path
    output_path = args.output

    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Write cleaned content to output file
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_content)

    print(f"Cleaned markdown saved to {output_path}")


if __name__ == "__main__":
    main()