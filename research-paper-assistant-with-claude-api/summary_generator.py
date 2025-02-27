# summary_generator.py
from anthropic import Anthropic
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
client = Anthropic(api_key=ANTHROPIC_API_KEY)


def generate_summary(paper_data, level='intermediate'):
    """
    Generate a summary of a paper at the specified expertise level.

    Args:
        paper_data (list): List of paper sections with metadata
        level (str): 'beginner', 'intermediate', or 'advanced'

    Returns:
        str: Generated summary
    """
    # Extract metadata from the first section
    metadata = paper_data[0]['metadata']
    title = metadata.get('title', 'Untitled Paper')
    authors = metadata.get('authors', [])
    if isinstance(authors, list):
        authors_str = ', '.join(authors)
    else:
        authors_str = authors

    # Extract text previews
    sections_text = ""
    for section in paper_data:
        section_name = section['section']
        preview = section['preview']
        sections_text += f"## {section_name}\n{preview}\n\n"

    # Determine level-specific instructions
    level_instructions = {
        'beginner': (
            "Create a summary for someone with no background in this field. "
            "Define all technical terms, use simple analogies, and focus on the big picture. "
            "Avoid jargon and explain the significance clearly."
        ),
        'intermediate': (
            "Create a summary for someone with basic knowledge of this field. "
            "Technical terms can be used but briefly explained. "
            "Include methodology overview and main findings."
        ),
        'advanced': (
            "Create a summary for domain experts. "
            "Use proper technical terminology, focus on novel contributions, "
            "methodological innovations, and relationship to other research in the field. "
            "Be precise and detailed."
        )
    }

    instruction = level_instructions.get(level, level_instructions['intermediate'])

    # Create prompt
    prompt = f"""
    Paper Title: {title}
    Authors: {authors_str}

    Paper Content:
    {sections_text}

    {instruction}

    Please provide a concise summary (about 500 words) that includes:
    1. Main research question or objective
    2. Key methodologies used
    3. Major findings
    4. Significance and implications
    """

    # Get response from Claude
    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text


# Example usage
if __name__ == "__main__":
    # Test with dummy data
    paper_data = [{
        'metadata': {
            'title': 'Test Paper on AI Agents',
            'authors': ['John Doe', 'Jane Smith'],
        },
        'section': 'ABSTRACT',
        'preview': 'This paper explores the development of AI agents...'
    }]

    summary = generate_summary(paper_data, 'intermediate')
    print(summary)