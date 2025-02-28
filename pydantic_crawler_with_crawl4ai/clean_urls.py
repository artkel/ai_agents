import re
import os


def clean_urls_from_markdown(input_file, output_file=None):
    """
    Removes lines containing URLs from a markdown file.

    Args:
        input_file (str): Path to the input markdown file
        output_file (str, optional): Path to the output cleaned file. If None, will modify the input file.
    """
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} does not exist")
        return

    if output_file is None:
        output_file = input_file + '.clean.md'

    # URL patterns to match
    url_patterns = [
        r'https?://[^\s)]+',  # Standard URLs
        r'<https?://[^\s>]+>',  # URLs in angle brackets
    ]

    print(f"Cleaning URLs from {input_file}")

    # Read the file content
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Filter out lines with URLs
    cleaned_lines = []
    removed_count = 0

    for line in lines:
        # Check if the line contains a URL pattern
        contains_url = any(re.search(pattern, line) for pattern in url_patterns)

        # Special case for markdown link format: [text](url)
        contains_md_link = re.search(r'\[[^\]]+\]\([^)]+\)', line)

        # Special case for navigation links like "- [link](#anchor)"
        # We want to keep these, but only if they're internal links (no http)
        internal_link = re.search(r'\[[^\]]+\]\(#[^)]+\)', line)

        if contains_url and not (internal_link and not contains_url):
            removed_count += 1
            continue

        # For markdown links, check if they contain external URLs
        if contains_md_link and not internal_link:
            # Extract the URL part and check if it's an external URL
            url_part = re.search(r'\([^)]+\)', line)
            if url_part and re.search(r'https?://', url_part.group(0)):
                removed_count += 1
                continue

        # Keep lines with no URLs or only internal links
        cleaned_lines.append(line)

    # Write the cleaned content
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(cleaned_lines)

    print(f"Removed {removed_count} lines containing URLs")
    print(f"Cleaned content saved to {output_file}")


if __name__ == "__main__":
    # Define the input and output paths
    input_file = "_combined_pydantic_docs.md"  # The combined markdown file
    output_file = "_combined_pydantic_docs_clean.md"  # The cleaned output file

    clean_urls_from_markdown(input_file, output_file)