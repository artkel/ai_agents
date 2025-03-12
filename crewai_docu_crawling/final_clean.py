#!/usr/bin/env python3
"""
Enhanced script specifically for removing empty links from the documentation.
Run this after the main cleaner if empty links still remain.
"""

import os
import re
import argparse


def remove_empty_links(content):
    """
    Focuses specifically on removing empty links with various patterns.
    """
    # First pass with standard regex
    content = re.sub(r'\[\s*\]\s*\(\s*https://.*?\)', '', content)

    # Second pass specific to docs.crewai.com
    content = re.sub(r'\[\s*\]\s*\(\s*https://docs\.crewai\.com.*?\)', '', content)

    # Third pass with more aggressive pattern matching
    pattern = r'\[.*?\]\(https://docs\.crewai\.com[^)]*\)'
    content = re.sub(pattern, '', content)

    # Fourth pass line by line approach
    lines = content.split('\n')
    cleaned_lines = []

    for line in lines:
        if not re.search(r'\[\s*\]\s*\(', line):
            cleaned_lines.append(line)

    return '\n'.join(cleaned_lines)


def main():
    parser = argparse.ArgumentParser(description='Enhanced script for removing empty links.')
    parser.add_argument('--input_file', default='output/crewai_documentation_clean.md',
                        help='Input markdown file to process (default: output/crewai_documentation_clean.md)')
    parser.add_argument('-o', '--output', default='output/crewai_documentation_final.md',
                        help='Output file path (default: output/crewai_documentation_final.md)')

    args = parser.parse_args()

    # Read input file
    try:
        with open(args.input_file, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Error: Input file '{args.input_file}' not found.")
        return

    # Process the content
    cleaned_content = remove_empty_links(content)

    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    # Write cleaned content to output file
    with open(args.output, 'w', encoding='utf-8') as file:
        file.write(cleaned_content)

    print(f"Final cleaned markdown saved to {args.output}")


if __name__ == "__main__":
    main()