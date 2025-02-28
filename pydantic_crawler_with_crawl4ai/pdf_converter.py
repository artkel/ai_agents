import markdown
from weasyprint import HTML, CSS
import os
import sys
from pathlib import Path


def markdown_to_pdf(markdown_file, output_file=None, css_file=None):
    """
    Convert a markdown file to PDF using WeasyPrint.

    Args:
        markdown_file (str): Path to the markdown file
        output_file (str, optional): Path to the output PDF file. If None, will use the markdown filename with .pdf extension.
        css_file (str, optional): Path to a CSS file for styling the PDF. If None, will use default styles.
    """
    if not os.path.exists(markdown_file):
        print(f"Error: Markdown file {markdown_file} does not exist")
        return

    # Set default output filename if not provided
    if output_file is None:
        output_file = Path(markdown_file).with_suffix('.pdf')

    print(f"Converting {markdown_file} to {output_file}")

    # Read the markdown content
    with open(markdown_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Convert markdown to HTML
    html_content = markdown.markdown(
        md_content,
        extensions=[
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc'
        ]
    )

    # Add HTML wrapper with proper styling
    html_doc = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Pydantic Documentation</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 2cm;
            }}
            h1, h2, h3, h4, h5, h6 {{
                color: #333;
                margin-top: 1.5em;
                margin-bottom: 0.5em;
            }}
            h1 {{ font-size: 2.2em; }}
            h2 {{ font-size: 1.8em; }}
            h3 {{ font-size: 1.5em; }}
            h4 {{ font-size: 1.3em; }}
            p {{ margin: 1em 0; }}
            pre {{
                background-color: #f5f5f5;
                padding: 1em;
                border-radius: 5px;
                overflow-x: auto;
            }}
            code {{
                font-family: Consolas, Monaco, 'Andale Mono', monospace;
                background-color: #f5f5f5;
                padding: 0.2em 0.4em;
                border-radius: 3px;
            }}
            pre code {{
                background-color: transparent;
                padding: 0;
            }}
            table {{
                border-collapse: collapse;
                margin: 1em 0;
                width: 100%;
            }}
            table, th, td {{
                border: 1px solid #ddd;
            }}
            th, td {{
                padding: 0.5em;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
            }}
            a {{
                color: #0366d6;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
            img {{
                max-width: 100%;
            }}
            hr {{
                border: none;
                border-top: 1px solid #ddd;
                margin: 2em 0;
            }}
            blockquote {{
                border-left: 4px solid #ddd;
                padding-left: 1em;
                margin-left: 0;
                color: #666;
            }}
            @page {{
                size: A4;
                margin: 2cm;
                @bottom-center {{
                    content: counter(page);
                }}
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    # Load custom CSS if provided
    css = None
    if css_file and os.path.exists(css_file):
        css = CSS(filename=css_file)

    # Create PDF
    try:
        HTML(string=html_doc).write_pdf(output_file, stylesheets=[css] if css else None)
        print(f"PDF conversion successful! File saved at: {output_file}")
        return True
    except Exception as e:
        print(f"Error converting to PDF: {e}")
        return False


if __name__ == "__main__":
    # If run from command line, allow specifying the input file
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = "_combined_pydantic_docs_clean.md"  # Default input file

    # Optional output file as second argument
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    # Optional CSS file as third argument
    css_file = sys.argv[3] if len(sys.argv) > 3 else None

    markdown_to_pdf(input_file, output_file, css_file)