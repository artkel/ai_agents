# embeddings.py
import os
import json
import numpy as np
import faiss
import pickle
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")


class EmbeddingManager:
    def __init__(self, embedding_dir="embeddings", model="text-embedding-3-small"):
        """
        Initialize the embedding manager.

        Args:
            embedding_dir (str): Directory to store embeddings and index
            model (str): Name of the OpenAI embedding model to use
        """
        # Create embeddings directory if it doesn't exist
        self.embedding_dir = embedding_dir
        os.makedirs(embedding_dir, exist_ok=True)

        # Initialize OpenAI client
        self.client = OpenAI(api_key=OPENAI_API_KEY)

        # Set embedding model
        self.model = model
        print(f"Using embedding model: {self.model}")

        # Set embedding dimension based on the model
        self.dimension = 1536  # Default for text-embedding-3-small
        print(f"Embedding dimension: {self.dimension}")

        # Path to the FAISS index file
        self.index_path = os.path.join(embedding_dir, "paper_index.faiss")

        # Path to metadata file
        self.metadata_path = os.path.join(embedding_dir, "paper_metadata.pkl")

        # Initialize or load index
        self.index = None
        self.load_or_create_index()

        # Initialize or load metadata
        self.metadata = []
        self.load_metadata()

    def load_or_create_index(self):
        """Load existing FAISS index or create a new one."""
        if os.path.exists(self.index_path):
            try:
                self.index = faiss.read_index(self.index_path)
                print(f"Loaded existing index with {self.index.ntotal} vectors")
            except Exception as e:
                print(f"Error loading index: {e}")
                self.create_new_index()
        else:
            self.create_new_index()

    def create_new_index(self):
        """Create a new FAISS index."""
        # Create a new index - using cosine similarity
        self.index = faiss.IndexFlatIP(self.dimension)  # Inner product for cosine similarity
        print("Created new FAISS index")

    def load_metadata(self):
        """Load metadata about stored embeddings."""
        if os.path.exists(self.metadata_path):
            try:
                with open(self.metadata_path, 'rb') as f:
                    self.metadata = pickle.load(f)
                print(f"Loaded metadata for {len(self.metadata)} embeddings")
            except Exception as e:
                print(f"Error loading metadata: {e}")
                self.metadata = []
        else:
            self.metadata = []

    def save_index(self):
        """Save the FAISS index to disk."""
        try:
            faiss.write_index(self.index, self.index_path)
            print(f"Saved index with {self.index.ntotal} vectors")
        except Exception as e:
            print(f"Error saving index: {e}")

    def save_metadata(self):
        """Save metadata about stored embeddings."""
        try:
            with open(self.metadata_path, 'wb') as f:
                pickle.dump(self.metadata, f)
            print(f"Saved metadata for {len(self.metadata)} embeddings")
        except Exception as e:
            print(f"Error saving metadata: {e}")

    def generate_embedding(self, text):
        """
        Generate embedding for a piece of text using OpenAI's API.

        Args:
            text (str): Text to embed

        Returns:
            numpy.ndarray: Embedding vector
        """
        try:
            # Truncate text if too long (OpenAI has token limits)
            max_chars = 8000  # Rough approximation: 4 chars per token
            if len(text) > max_chars:
                text = text[:max_chars]

            # Get embedding from OpenAI API
            response = self.client.embeddings.create(
                model=self.model,
                input=text,
                encoding_format="float"
            )

            # Extract embedding vector
            embedding = np.array(response.data[0].embedding, dtype=np.float32)

            # Normalize for cosine similarity
            faiss.normalize_L2(embedding.reshape(1, -1))

            return embedding

        except Exception as e:
            print(f"Error generating embedding: {e}")
            return None

    def add_paper_sections(self, paper_id, sections, metadata):
        """
        Add paper sections to the index.

        Args:
            paper_id (str): Unique ID for the paper
            sections (dict): Dictionary of section name -> section text
            metadata (dict): Paper metadata

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            for section_name, section_text in sections.items():
                # Skip very short sections or empty sections
                if len(section_text.strip()) < 50:
                    continue

                # Generate embedding
                embedding = self.generate_embedding(section_text)
                if embedding is None:
                    continue

                # Add to index
                self.index.add(embedding.reshape(1, -1))

                # Store metadata
                self.metadata.append({
                    "paper_id": paper_id,
                    "section": section_name,
                    "metadata": metadata,
                    # Store the first 200 chars of the section for verification
                    "preview": section_text[:200].replace("\n", " ")
                })

            # Save updated index and metadata
            self.save_index()
            self.save_metadata()
            return True

        except Exception as e:
            print(f"Error adding paper sections: {e}")
            return False

    def search(self, query, k=5):
        """
        Search for most similar sections to the query.

        Args:
            query (str): Search query
            k (int): Number of results to return

        Returns:
            list: List of dictionaries with search results
        """
        try:
            # Generate embedding for the query
            query_embedding = self.generate_embedding(query)
            if query_embedding is None:
                return []

            # Search the index
            distances, indices = self.index.search(query_embedding.reshape(1, -1), k)

            # Format results
            results = []
            for i, idx in enumerate(indices[0]):
                if idx < len(self.metadata) and idx >= 0:
                    result = self.metadata[idx].copy()
                    result["score"] = float(distances[0][i])  # Higher is better for cosine similarity
                    results.append(result)

            return results

        except Exception as e:
            print(f"Error searching: {e}")
            return []


# Example usage
if __name__ == "__main__":
    import sys

    sys.path.append('.')  # Make sure Python can find modules in the current directory
    from pdf_processor import process_paper
    import uuid

    # Create embedding manager
    em = EmbeddingManager()

    # Process a paper
    pdf_path = "data/test_document.pdf"
    full_text, sections, metadata = process_paper(pdf_path)

    # Generate a unique ID for the paper
    paper_id = str(uuid.uuid4())

    # Add paper sections to the index
    print(f"Adding paper sections to index...")
    success = em.add_paper_sections(paper_id, sections, metadata)
    print(f"Added paper with ID: {paper_id}")

    # Now try searching
    query = "elastic system"
    results = em.search(query, k=3)
    print(f"\nSearch results for '{query}':")
    print(f"Found {len(results)} results")
    for i, result in enumerate(results):
        print(f"Result {i + 1}:")
        print(f"  Paper: {result['metadata']['title']}")
        print(f"  Section: {result['section']}")
        print(f"  Score: {result['score']}")
        print(f"  Preview: {result['preview']}...")
        print()