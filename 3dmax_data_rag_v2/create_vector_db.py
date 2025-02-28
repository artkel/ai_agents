import json
import os
import numpy as np
import faiss
import pickle
from sentence_transformers import SentenceTransformer
import html
import re


def clean_html_tags(text):
    """Remove HTML tags from text and decode HTML entities."""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Decode HTML entities
    text = html.unescape(text)
    return text


class EmbeddingEngine:
    def __init__(self, model_name="paraphrase-multilingual-mpnet-base-v2"):
        """Initialize the embedding engine with a multilingual model."""
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)

    def get_embeddings(self, texts):
        """Generate embeddings for a list of texts."""
        # Clean HTML tags from texts
        clean_texts = [clean_html_tags(text) for text in texts]

        # Generate embeddings
        embeddings = self.model.encode(clean_texts, show_progress_bar=True)

        return embeddings


def prepare_documents(qa_data):
    """Prepare documents for embedding and retrieval."""
    documents = []
    metadata = []

    for qa_pair in qa_data:
        # Create a document that combines question and answer for better semantic matching
        doc_text = f"Вопрос: {qa_pair['question']}\nОтвет: {qa_pair['answer']}"

        # Store the document text for embedding
        documents.append(doc_text)

        # Store metadata for retrieval
        metadata.append({
            "id": qa_pair["id"],
            "question": qa_pair["question"],
            "answer": qa_pair["answer"],
            "media": qa_pair["media"],
            "links": qa_pair["links"]
        })

    return documents, metadata


def create_faiss_index(embeddings):
    """Create a FAISS index for fast similarity search."""
    # Get the embedding dimension
    dimension = embeddings.shape[1]

    # Create an L2 distance index (Euclidean distance)
    index = faiss.IndexFlatL2(dimension)

    # Add embeddings to the index
    index.add(embeddings.astype(np.float32))

    return index


def save_vector_db(index, documents, metadata, output_dir="vector_db"):
    """Save the vector database and supporting data."""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Save FAISS index
    faiss.write_index(index, os.path.join(output_dir, "faiss_index.bin"))
    print(f"Saved FAISS index to {output_dir}/faiss_index.bin")

    # Save documents and metadata
    with open(os.path.join(output_dir, "documents.pkl"), "wb") as f:
        pickle.dump(documents, f)
    print(f"Saved documents to {output_dir}/documents.pkl")

    with open(os.path.join(output_dir, "metadata.pkl"), "wb") as f:
        pickle.dump(metadata, f)
    print(f"Saved metadata to {output_dir}/metadata.pkl")


def main():
    import re  # Import here to avoid global scope issues

    # Load the Q&A data
    input_file = "data/qa_data.json"
    print(f"Loading Q&A data from {input_file}")

    with open(input_file, "r", encoding="utf-8") as f:
        qa_data = json.load(f)

    print(f"Loaded {len(qa_data)} Q&A pairs")

    # Prepare documents and metadata
    documents, metadata = prepare_documents(qa_data)
    print(f"Prepared {len(documents)} documents for embedding")

    # Initialize embedding engine
    embedding_engine = EmbeddingEngine()

    # Generate embeddings
    print("Generating embeddings...")
    embeddings = embedding_engine.get_embeddings(documents)
    print(f"Generated embeddings with shape: {embeddings.shape}")

    # Create FAISS index
    print("Creating FAISS index...")
    index = create_faiss_index(embeddings)
    print(f"Created FAISS index with {index.ntotal} vectors")

    # Save vector database
    output_dir = "vector_db"
    save_vector_db(index, documents, metadata, output_dir)

    print(f"Vector database created successfully in {output_dir}")


if __name__ == "__main__":
    main()