import os
import re
from urllib.parse import unquote


def combine_markdown_files(input_dir, output_file):
    """
    Combines all markdown files in the input directory into a single markdown file.

    Args:
        input_dir (str): Path to the directory containing markdown files
        output_file (str): Path to the output combined markdown file
    """
    # Ensure input directory exists
    if not os.path.exists(input_dir):
        print(f"Error: Input directory {input_dir} does not exist")
        return

    # Get all markdown files
    md_files = [f for f in os.listdir(input_dir) if f.endswith('.md')]

    if not md_files:
        print(f"No markdown files found in {input_dir}")
        return

    print(f"Found {len(md_files)} markdown files to combine")

    # Sort files to maintain a logical order
    md_files.sort()

    # Extract title from filename for table of contents
    toc_entries = []
    for file in md_files:
        # Convert filename to a more readable title
        title = os.path.splitext(file)[0]  # Remove extension
        title = title.replace('_', ' ')  # Replace underscores with spaces
        title = unquote(title)  # URL decode
        title = re.sub(r'\s+', ' ', title).strip()  # Clean up whitespace

        # Create anchor from filename
        anchor = file.replace('.md', '').lower()

        toc_entries.append((title, anchor, file))

    # Write combined file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Write title
        outfile.write("# Combined Pydantic Documentation\n\n")

        # Write table of contents
        outfile.write("## Table of Contents\n\n")

        for title, anchor, _ in toc_entries:
            outfile.write(f"- [{title}](#{anchor})\n")

        outfile.write("\n---\n\n")

        # Write content from each file
        for title, anchor, file in toc_entries:
            file_path = os.path.join(input_dir, file)

            outfile.write(f"<a id='{anchor}'></a>\n\n")
            outfile.write(f"## {title}\n\n")

            try:
                with open(file_path, 'r', encoding='utf-8') as infile:
                    # Skip first line if it's a title/header (to avoid duplication)
                    content = infile.read()

                    # If content starts with a # header that matches our title, skip it
                    if content.startswith('# '):
                        first_line_end = content.find('\n')
                        if first_line_end > 0:
                            content = content[first_line_end + 1:].strip()

                    outfile.write(content)
                    outfile.write("\n\n---\n\n")
            except Exception as e:
                outfile.write(f"*Error reading file: {e}*\n\n---\n\n")

    print(f"Combined markdown saved to {output_file}")


if __name__ == "__main__":
    # Define the input and output paths
    input_directory = "output"  # The directory with your markdown files
    output_file = "_combined_pydantic_docs.md"  # The name of the combined file

    combine_markdown_files(input_directory, output_file)