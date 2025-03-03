import re
import os


def clean_markdown_file(input_file, output_file=None):
    """
    Cleans a markdown file by:
    1. Removing lines that contain only numbers
    2. Removing lines containing external URLs of the form '](https:'
    3. Cleaning up consecutive empty lines

    Args:
        input_file (str): Path to the input markdown file
        output_file (str, optional): Path to the output cleaned file. If None, will use a default name.
    """
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} does not exist")
        return False

    if output_file is None:
        output_file = input_file.replace('.md', '_clean.md')

    print(f"Cleaning {input_file}")

    # Read the file content
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Filter out unwanted lines
    cleaned_lines = []
    empty_line_count = 0
    number_line_count = 0
    url_line_count = 0

    for line in lines:
        # Check if the line contains only numbers
        if re.match(r'^\s*\d+\s*$', line):
            number_line_count += 1
            continue

        # Check if the line contains an external URL link
        if '](https:' in line or '](http:' in line:
            url_line_count += 1
            continue

        # Check if the line is empty or contains only whitespace
        if line.strip() == '':
            empty_line_count += 1
            # Keep only one empty line between content
            if empty_line_count <= 1:
                cleaned_lines.append(line)
        else:
            # This is a content line, reset empty line counter
            empty_line_count = 0
            cleaned_lines.append(line)

    # Clean up any trailing empty lines
    while cleaned_lines and cleaned_lines[-1].strip() == '':
        cleaned_lines.pop()

    # Write the cleaned content
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(cleaned_lines)

    print(f"Cleaning complete:")
    print(f"- Removed {number_line_count} number-only lines")
    print(f"- Removed {url_line_count} URL-containing lines")
    print(f"- Normalized empty lines")
    print(f"Cleaned content saved to {output_file}")

    return True


if __name__ == "__main__":
    # Define input and output files
    # Change this to your actual file name
    input_file = "pydanticai_documentation.md"
    output_file = "pydanticai_documentation_clean.md"

    clean_markdown_file(input_file, output_file)