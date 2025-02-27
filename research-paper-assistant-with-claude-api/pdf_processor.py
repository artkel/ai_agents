import re
import os
import PyPDF2
from anthropic import Anthropic
from config import ANTHROPIC_API_KEY

# Initialize the Anthropic client for Claude API
client = Anthropic(api_key=ANTHROPIC_API_KEY)

# Get the directory where the current script is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Build path to the data directory
data_dir = os.path.join(current_dir, "data")

# Build the full path to the PDF
pdf_path = os.path.join(data_dir, "test_document.pdf")

def extract_text_from_pdf(pdf_path):
    """
    Extract all text from a PDF file.

    Args:
        pdf_path (str): Path to the PDF file

    Returns:
        str: Extracted text content
    """
    # Initialize an empty string to store all text
    text = ""

    try:
        # Open the PDF file in read-binary mode
        with open(pdf_path, 'rb') as file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(file)

            # Get total number of pages
            num_pages = len(pdf_reader.pages)

            # Loop through each page and extract text
            for page_num in range(num_pages):
                # Get the page object
                page = pdf_reader.pages[page_num]

                # Extract text from the page and add to our text string
                page_text = page.extract_text()
                text += page_text + "\n\n"  # Add a separator between pages

        return text

    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def identify_sections(text):
    """
    Split the research paper text into logical sections.

    Args:
        text (str): Full text of the paper

    Returns:
        dict: Dictionary with section names as keys and content as values
    """
    # Initialize dictionary to store sections
    sections = {}

    # Common section headers in research papers
    section_patterns = [
        r"ABSTRACT",
        r"INTRODUCTION",
        r"LITERATURE REVIEW",
        r"RELATED WORK",
        r"BACKGROUND",
        r"METHODOLOGY|METHODS",
        r"EXPERIMENTAL SETUP|EXPERIMENTS",
        r"RESULTS",
        r"DISCUSSION",
        r"CONCLUSION",
        r"REFERENCES|BIBLIOGRAPHY"
    ]

    # Create a regex pattern that matches any of the section headers
    # \n ensures we match section headers at the start of a line
    # Move the (?i) to the beginning of the pattern
    combined_pattern = r"(?i)\n(" + "|".join(section_patterns) + r")[:\s\n]"

    # Find all potential section headers in the text
    matches = list(re.finditer(combined_pattern, text))

    # If no sections found, treat the entire document as a single section
    if not matches:
        sections["FULL_TEXT"] = text
        return sections

    # Process each section
    for i in range(len(matches)):
        # Get current match
        current_match = matches[i]

        # Get the section name (removing leading/trailing whitespace and converting to uppercase)
        section_name = text[current_match.start():current_match.end()].strip().upper()

        # Clean up the section name
        section_name = re.sub(r"[:\s\n]", "", section_name)

        # Determine the section content
        # If this is the last section, content goes until the end of the document
        if i == len(matches) - 1:
            section_content = text[current_match.end():]
        else:
            # Otherwise, content goes until the start of the next section
            next_match = matches[i + 1]
            section_content = text[current_match.end():next_match.start()]

        # Store in the dictionary
        sections[section_name] = section_content.strip()

    return sections

# text = extract_text_from_pdf(pdf_path)


def extract_metadata(text, pdf_path):
    """
    Extract metadata from the research paper.

    Args:
        text (str): The full text of the paper
        pdf_path (str): Path to the PDF file

    Returns:
        dict: Dictionary containing metadata fields
    """
    # Get basic file info
    file_name = os.path.basename(pdf_path)
    file_size = os.path.getsize(pdf_path)

    # Initialize metadata with file info
    metadata = {
        "filename": file_name,
        "file_size_bytes": file_size,
    }

    # Get first 2000 characters for analysis where metadata usually appears
    first_part = text[:2000]

    # Use Claude to extract metadata from the beginning of the paper
    prompt = f"""
    Extract the following metadata from this research paper text. If you can't find a piece of information, leave it as null or N/A.

    Research paper beginning:
    ---
    {first_part}
    ---

    Please format your response as a clearly structured JSON with these fields:
    - title: The title of the paper
    - authors: List of authors
    - publication_date: When the paper was published
    - journal: Name of the journal or conference
    - doi: DOI if present
    - keywords: List of keywords if present
    """

    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )

        # Extract JSON from response
        response_text = response.content[0].text

        # Find JSON using regex
        import json
        import re

        # Look for JSON structure in the response
        json_match = re.search(r'({[\s\S]*})', response_text)

        if json_match:
            extracted_metadata = json.loads(json_match.group(1))
            metadata.update(extracted_metadata)
        else:
            print("Could not extract metadata JSON from Claude's response")

    except Exception as e:
        print(f"Error extracting metadata with Claude: {e}")

    return metadata



def process_paper(pdf_path):
    """
    Process a research paper: extract text, identify sections, and extract metadata.

    Args:
        pdf_path (str): Path to the PDF file

    Returns:
        tuple: (full_text, sections, metadata)
    """
    # Extract text from PDF
    full_text = extract_text_from_pdf(pdf_path)

    # Split into sections
    sections = identify_sections(full_text)

    # Extract metadata
    metadata = extract_metadata(full_text, pdf_path)

    return full_text, sections, metadata


# Example usage:
if __name__ == "__main__":
    # Test the module with a sample PDF
    # sample_pdf = "path/to/your/sample_paper.pdf"
    text, sections, metadata = process_paper(pdf_path)

    print(f"Extracted {len(text)} characters of text")
    print(f"Identified {len(sections)} sections: {list(sections.keys())}")
    print(f"Metadata: {metadata}")
