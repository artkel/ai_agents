# main.py
import os
import uuid
from pdf_processor import process_paper
from embeddings import EmbeddingManager
from summary_generator import generate_summary
from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'data'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize embedding manager
embedding_manager = EmbeddingManager()

# Define allowed file extensions
ALLOWED_EXTENSIONS = {'pdf'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Process the paper
        try:
            full_text, sections, metadata = process_paper(filepath)

            # Generate a unique ID for the paper
            paper_id = str(uuid.uuid4())

            # Add to embedding index
            success = embedding_manager.add_paper_sections(paper_id, sections, metadata)

            if success:
                return jsonify({
                    'success': True,
                    'paper_id': paper_id,
                    'metadata': metadata,
                    'sections': list(sections.keys())
                })
            else:
                return jsonify({'error': 'Failed to index paper'}), 500

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'Invalid file type'}), 400


@app.route('/search', methods=['POST'])
def search():
    data = request.json
    if not data or 'query' not in data:
        return jsonify({'error': 'No query provided'}), 400

    query = data['query']
    k = data.get('limit', 5)

    # Perform search
    results = embedding_manager.search(query, k=k)

    return jsonify({'results': results})


@app.route('/summary', methods=['POST'])
def summarize():
    data = request.json
    if not data or 'paper_id' not in data:
        return jsonify({'error': 'No paper ID provided'}), 400

    paper_id = data['paper_id']
    level = data.get('level', 'intermediate')  # beginner, intermediate, advanced

    # Get paper sections from search results
    results = embedding_manager.search(paper_id, k=100)  # Use paper_id as query to find all sections

    # Filter results for this paper
    paper_sections = [r for r in results if r['paper_id'] == paper_id]

    if not paper_sections:
        return jsonify({'error': 'Paper not found'}), 404

    # Extract full text from sections
    section_texts = {}
    for section in paper_sections:
        # Here we'd need to retrieve the full section text
        # This is a placeholder - in a real implementation, we'd store this
        pass

    # Generate summary
    summary = generate_summary(paper_sections, level)

    return jsonify({'summary': summary})


if __name__ == '__main__':
    app.run(debug=True)