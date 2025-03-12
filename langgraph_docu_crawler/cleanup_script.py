import re
import os


def clean_langgraph_documentation(input_file, output_file):
    """
    Clean up the Langgraph documentation markdown file by:
    1. Removing [](https://langchain-ai.github.io/langgraph/...) prefixes from code snippets
    2. Removing navigation-related and menu-related lines
    3. Removing bullet points with links and nothing else
    4. Removing footer content, copyright information, etc.
    5. Cleaning up any remaining URLs in various formats

    Args:
        input_file (str): Path to the input markdown file
        output_file (str): Path to save the cleaned output
    """
    print(f"Cleaning {input_file}...")

    # Read the content of the file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read().splitlines()

    cleaned_lines = []

    # Extended list of unwanted patterns
    unwanted_patterns = [
        "Skip to content",
        "Join us at",
        "Initializing search",
        "Go to repository",
        "Home",
        "API reference",
        "Get started",
        "Guides",
        "Tutorials",
        "Resources",
        "Table of contents",
        "![logo]",
        "Was this page helpful?",
        "Thanks for your feedback!",
        "Please help us improve",
        "Back to top",
        "Previous",
        "Next",
        "Copyright",
        "Made with",
        "Consent Preferences",
        "Cookie consent",
        "We use cookies",
        "Accept Reject",
        "Google Analytics",
        "GitHub"
    ]

    for line in content:
        # Skip lines containing unwanted navigation elements
        if any(pattern in line for pattern in unwanted_patterns):
            continue

        # Skip bullet points or numbered lists that are just links with nothing else
        if re.match(r'^\s*[\*\d\.]\s+\[\s.*?\]\(https?://.*?\)\s*$', line):
            continue

        # Skip lines that are just standalone links with nothing else
        if re.match(r'^\s*\[\s.*?\]\(https?://.*?\)\s*$', line):
            continue

        # Remove code line reference prefixes
        if re.match(r'\[\]\(https://langchain-ai\.github\.io/langgraph/.*?\)', line):
            code_part = re.sub(r'^\[\]\(https://langchain-ai\.github\.io/langgraph/.*?\)\s*', '', line)
            if code_part.strip():  # Only add non-empty lines
                cleaned_lines.append(code_part)
            continue

        # Remove any remaining URLs in parentheses (https://...)
        line = re.sub(r'\(https?://[^\)]*\)', '', line)

        # Remove any remaining text URLs without parentheses
        line = re.sub(r'https?://\S+', '', line)

        # Remove any resulting empty Markdown links [text]()
        line = re.sub(r'\[([^\]]*)\]\(\)', r'\1', line)

        # Only add non-empty lines after all substitutions
        if line.strip():
            cleaned_lines.append(line)

    # Write the cleaned content to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(cleaned_lines))

    print(f"Cleaned documentation saved to {output_file}")
    print(f"Removed {len(content) - len(cleaned_lines)} lines")


if __name__ == "__main__":
    # Use the output folder for both input and output files
    input_file = os.path.join("output", "langgraph_documentation_raw.md")
    output_file = os.path.join("output", "langgraph_documentation_cleaned.md")

    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    if not os.path.exists(input_file):
        print(f"Error: The file {input_file} does not exist.")
    else:
        clean_langgraph_documentation(input_file, output_file)