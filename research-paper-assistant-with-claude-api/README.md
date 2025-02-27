# Research Paper Assistant

A web-based tool for processing, searching, and summarizing academic papers using AI technologies.

## Features

- **PDF Processing**: Extract text and metadata from research papers
- **Semantic Search**: Find relevant sections across all indexed papers
- **Multi-Level Summaries**: Generate concise summaries for different expertise levels (beginner, intermediate, advanced)
- **Simple Web Interface**: Upload, search, and summarize papers through an intuitive UI

## Technology Stack

- **Backend**: Python, Flask
- **Embeddings**: OpenAI API (text-embedding-3-small)
- **Summarization**: Anthropic Claude API (claude-3-haiku-20240307)
- **Vector Database**: FAISS for efficient similarity search
- **Frontend**: HTML, Bootstrap, JavaScript

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/research-paper-assistant.git
   cd research-paper-assistant
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install flask anthropic openai faiss-cpu numpy python-dotenv PyPDF2
   ```

4. Create a `.env` file with your API keys:
   ```
   ANTHROPIC_API_KEY=your_anthropic_key
   OPENAI_API_KEY=your_openai_key
   ```

## Usage

1. Start the application:
   ```bash
   python main.py
   ```

2. Open your browser and navigate to: http://127.0.0.1:5000

3. Use the interface to:
   - Upload PDF research papers
   - Search across all indexed papers
   - Generate summaries at different expertise levels

## Project Structure

- `main.py`: Flask application and main logic
- `pdf_processor.py`: Handles PDF text extraction and section identification
- `embeddings.py`: Manages vector embeddings and search functionality 
- `summary_generator.py`: Generates paper summaries using Claude API
- `templates/`: HTML templates for the web interface
- `data/`: Storage location for uploaded papers
- `embeddings/`: Storage for vector database and metadata

## Notes

- This application is designed for research and educational purposes
- The quality of embeddings and summaries depends on the APIs used
- Large papers may be truncated due to API context limits

## Future Improvements

- Add user authentication
- Implement paper comparison functionality 
- Improve section detection for better search results
- Add citation generation in various formats
- Support for more document types (DOCX, arXiv, etc.)

## License

[MIT License](LICENSE)