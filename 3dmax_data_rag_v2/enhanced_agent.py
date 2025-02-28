import faiss
import pickle
import numpy as np
import os
import re
import html
from sentence_transformers import SentenceTransformer
import json


class Agent3DMax:
    def __init__(self, vector_db_path="vector_db"):
        """Initialize the 3D Max Agent with the vector database."""
        self.vector_db_path = vector_db_path
        self.load_resources()
        self.load_model()
        self.create_keyword_index()

    def load_resources(self):
        """Load the vector database resources."""
        print(f"Loading resources from {self.vector_db_path}...")

        # Load FAISS index
        index_path = os.path.join(self.vector_db_path, "faiss_index.bin")
        self.index = faiss.read_index(index_path)
        print(f"Loaded FAISS index with {self.index.ntotal} vectors")

        # Load documents
        with open(os.path.join(self.vector_db_path, "documents.pkl"), "rb") as f:
            self.documents = pickle.load(f)
        print(f"Loaded {len(self.documents)} documents")

        # Load metadata
        with open(os.path.join(self.vector_db_path, "metadata.pkl"), "rb") as f:
            self.metadata = pickle.load(f)
        print(f"Loaded metadata for {len(self.metadata)} Q&A pairs")

    def load_model(self):
        """Load the sentence transformer model for embeddings."""
        model_name = "paraphrase-multilingual-mpnet-base-v2"
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)

    def create_keyword_index(self):
        """Create a keyword-based index for hybrid search."""
        self.keyword_index = {}

        # Important keywords in Russian for 3D Max operations
        keywords = ["сетка", "grid", "рендер", "rendering", "слой", "layer",
                    "панел", "panel", "настрой", "setting", "язык", "language",
                    "клавиш", "keyboard", "импорт", "import", "проект", "project",
                    "сохран", "save", "интерфейс", "interface"]

        # Create index mapping keywords to document indices
        for i, doc in enumerate(self.documents):
            doc_lower = doc.lower()

            # For each keyword, check if it's in the document
            for keyword in keywords:
                if keyword.lower() in doc_lower:
                    if keyword not in self.keyword_index:
                        self.keyword_index[keyword] = []
                    self.keyword_index[keyword].append(i)

        print(f"Created keyword index with {len(self.keyword_index)} keys")

    def clean_text(self, text):
        """Clean HTML tags from text and standardize whitespace."""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Decode HTML entities
        text = html.unescape(text)
        # Standardize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def generate_embedding(self, query):
        """Generate an embedding for a query."""
        # Clean the query
        clean_query = self.clean_text(query)
        # Generate embedding
        embedding = self.model.encode([clean_query])[0]
        return embedding

    def hybrid_search(self, query, top_k=3, threshold=0.15):
        """Perform hybrid search combining vector and keyword matching."""
        # Clean the query
        clean_query = self.clean_text(query.lower())

        # Generate query embedding
        query_embedding = self.generate_embedding(query)

        # Convert to float32 as required by FAISS
        query_embedding = np.array([query_embedding]).astype('float32')

        # Vector search
        distances, indices = self.index.search(query_embedding, top_k)

        # Initialize results dictionary
        results_dict = {}

        # Process vector search results
        for i in range(len(indices[0])):
            idx = indices[0][i]
            distance = distances[0][i]

            # Better similarity calculation from L2 distance
            similarity = np.exp(-distance / 10.0)

            # Skip results below threshold
            if similarity < threshold:
                continue

            # Add to results dictionary with vector score
            results_dict[idx] = {
                'metadata': self.metadata[idx],
                'document': self.documents[idx],
                'vector_similarity': similarity,
                'keyword_match': 0,
                'combined_score': similarity
            }

        # Keyword search boost
        for keyword in self.keyword_index:
            if keyword in clean_query:
                for idx in self.keyword_index[keyword]:
                    # If already in results, boost the score
                    if idx in results_dict:
                        results_dict[idx]['keyword_match'] += 0.1  # Keyword match bonus
                        results_dict[idx]['combined_score'] += 0.1
                    # If not in results, add it if it meets a lower threshold
                    elif len(results_dict) < top_k * 2:  # Allow some extra candidates
                        # Get the vector similarity
                        query_embedding_reshaped = np.reshape(query_embedding, (1, -1))
                        document_vector = self.index.reconstruct(idx)
                        document_vector_reshaped = np.reshape(document_vector, (1, -1))

                        # Calculate L2 distance
                        distance = np.linalg.norm(query_embedding_reshaped - document_vector_reshaped)
                        similarity = np.exp(-distance / 10.0)

                        # Add with keyword boost if it meets a lower threshold
                        if similarity > threshold * 0.7:  # Lower threshold for keyword matches
                            results_dict[idx] = {
                                'metadata': self.metadata[idx],
                                'document': self.documents[idx],
                                'vector_similarity': similarity,
                                'keyword_match': 0.1,  # Initial keyword match bonus
                                'combined_score': similarity + 0.1
                            }

        # Sort by combined score and convert to list
        results = sorted(results_dict.values(), key=lambda x: x['combined_score'], reverse=True)

        return results[:top_k]  # Return the top k results

    def format_response(self, result):
        """Format the response with answer, media, and links."""
        metadata = result['metadata']
        similarity = result['combined_score'] if 'combined_score' in result else result['similarity']

        # Format as Markdown for nice display
        response = [
            f"**Вопрос:** {metadata['question']}",
            f"**Ответ:** {metadata['answer']}"
        ]

        # Add media references if any
        if metadata['media']:
            response.append("\n**Медиа файлы:**")
            for media in metadata['media']:
                response.append(f"- {media}")

        # Add links if any
        if metadata['links']:
            response.append("\n**Дополнительная информация:**")
            for link in metadata['links']:
                response.append(f"- [{link}]({link})")

        # Add confidence information
        confidence = int(min(similarity * 100, 100))  # Cap at 100%
        response.append(f"\n*Релевантность: {confidence}%*")

        return "\n\n".join(response)

    def answer_question(self, query, threshold=0.15):
        """Answer a question about 3D Max."""
        # Hybrid search for relevant Q&A pairs
        results = self.hybrid_search(query, top_k=3, threshold=threshold)

        if not results:
            return (
                "Извините, я не нашел ответ на ваш вопрос в документации. "
                "Попробуйте переформулировать вопрос или обратитесь к руководству пользователя 3D Max."
            )

        # Return the best match
        best_match = results[0]

        # Check if it's a good match or a tentative match
        if best_match['combined_score'] > 0.4:  # Adjusted threshold for "good" match
            return self.format_response(best_match)
        else:
            # It's a tentative match
            return (
                    "Возможно, вы имели в виду:\n\n" +
                    self.format_response(best_match)
            )


def main():
    # Initialize the agent
    agent = Agent3DMax()

    print("\n=== 3D Max Assistant ===")
    print("Задайте вопрос о 3D Max или введите 'выход' для завершения.")

    # Main interaction loop
    while True:
        query = input("\nВопрос: ")

        # Check for exit command
        if query.lower() in ["выход", "exit", "quit", "q"]:
            print("До свидания!")
            break

        # Get answer
        answer = agent.answer_question(query)

        # Print answer
        print("\n" + answer)


if __name__ == "__main__":
    main()