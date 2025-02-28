import faiss
import pickle
import numpy as np
import os
import re
import html
import json
from sentence_transformers import SentenceTransformer


def load_and_check_resources(vector_db_path="vector_db"):
    """Load and inspect the vector database resources."""
    print(f"Loading resources from {vector_db_path}...")

    # Check if files exist
    index_path = os.path.join(vector_db_path, "faiss_index.bin")
    documents_path = os.path.join(vector_db_path, "documents.pkl")
    metadata_path = os.path.join(vector_db_path, "metadata.pkl")

    if not os.path.exists(index_path):
        print(f"ERROR: FAISS index not found at {index_path}")
        return None

    if not os.path.exists(documents_path):
        print(f"ERROR: Documents not found at {documents_path}")
        return None

    if not os.path.exists(metadata_path):
        print(f"ERROR: Metadata not found at {metadata_path}")
        return None

    # Load FAISS index
    index = faiss.read_index(index_path)
    print(f"Loaded FAISS index with {index.ntotal} vectors")

    # Load documents
    with open(documents_path, "rb") as f:
        documents = pickle.load(f)
    print(f"Loaded {len(documents)} documents")

    # Load metadata
    with open(metadata_path, "rb") as f:
        metadata = pickle.load(f)
    print(f"Loaded metadata for {len(metadata)} Q&A pairs")

    # Print a sample of the documents for inspection
    print("\nSample documents:")
    for i, doc in enumerate(documents[:3]):
        print(f"Document {i + 1}:\n{doc[:200]}...\n")

    # Print a sample of the metadata for inspection
    print("\nSample metadata:")
    for i, meta in enumerate(metadata[:3]):
        print(f"Metadata {i + 1}:\n{json.dumps(meta, ensure_ascii=False, indent=2)}\n")

    return index, documents, metadata


def test_embedding_and_search(query, index, documents, metadata):
    """Test embedding and search functionality."""
    # Initialize model
    model_name = "paraphrase-multilingual-mpnet-base-v2"
    print(f"Loading embedding model: {model_name}")
    model = SentenceTransformer(model_name)

    # Generate query embedding
    print(f"\nGenerating embedding for query: '{query}'")
    query_embedding = model.encode([query])[0]
    print(f"Generated embedding with shape: {query_embedding.shape}")

    # Convert to float32 as required by FAISS
    query_embedding = np.array([query_embedding]).astype('float32')

    # Search with different threshold values
    for threshold in [0.0, 0.3, 0.5, 0.7]:
        print(f"\n--- Searching with threshold {threshold} ---")
        # Search the index with a larger k to see more results
        k = 5
        distances, indices = index.search(query_embedding, k)

        # Process results
        for i in range(len(indices[0])):
            idx = indices[0][i]
            distance = distances[0][i]

            # Convert distance to similarity score
            similarity = 1.0 / (1.0 + distance)

            # Print result
            print(f"Result {i + 1}:")
            print(f"  Similarity: {similarity:.4f}")
            print(f"  L2 Distance: {distance:.4f}")
            if idx < len(metadata):
                print(f"  Question: {metadata[idx]['question']}")
                print(f"  Answer: {metadata[idx]['answer'][:100]}..." if len(
                    metadata[idx]['answer']) > 100 else f"  Answer: {metadata[idx]['answer']}")
            else:
                print(f"  ERROR: Index {idx} out of range for metadata")
            print()


def main():
    # Load and check resources
    result = load_and_check_resources()
    if not result:
        print("Failed to load resources. Please check the vector database.")
        return

    index, documents, metadata = result

    # Test queries
    queries = [
        "Как настроить отображение сетки (Grid)?",
        "Как изменить настройки сетки в 3D Max?",
        "Настройка сетки и её параметров",
        "Grid настройки"
    ]

    for query in queries:
        print("\n==================================================")
        print(f"TESTING QUERY: '{query}'")
        print("==================================================")
        test_embedding_and_search(query, index, documents, metadata)


if __name__ == "__main__":
    main()