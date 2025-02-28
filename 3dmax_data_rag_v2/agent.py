import faiss
import pickle
import numpy as np
import os
import re
import html
from sentence_transformers import SentenceTransformer


class Agent3DMax:
    def __init__(self, vector_db_path="vector_db"):
        """Initialize the 3D Max Agent with the vector database."""
        self.vector_db_path = vector_db_path
        self.load_resources()
        self.load_model()

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

    def search(self, query, top_k=3, threshold=0.15):
        """Search for the most relevant Q&A pairs for a query."""
        # Generate query embedding
        query_embedding = self.generate_embedding(query)

        # Convert to float32 as required by FAISS
        query_embedding = np.array([query_embedding]).astype('float32')

        # Search the index
        distances, indices = self.index.search(query_embedding, top_k)

        # Process results
        results = []
        for i in range(len(indices[0])):
            idx = indices[0][i]
            distance = distances[0][i]

            # Better similarity calculation from L2 distance
            # For L2 distance, smaller is better, so we use an exponential decay function
            # This gives more separation between close matches and distant matches
            similarity = np.exp(-distance / 10.0)  # Adjusted scale factor

            # Skip results below threshold
            if similarity < threshold:
                continue

            # Add to results
            results.append({
                'metadata': self.metadata[idx],
                'document': self.documents[idx],
                'similarity': similarity
            })

        return results

    def format_response(self, result):
        """Format the response with answer, media, and links."""
        metadata = result['metadata']
        similarity = result['similarity']

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
        confidence = int(similarity * 100)
        response.append(f"\n*Релевантность: {confidence}%*")

        return "\n\n".join(response)

    def answer_question(self, query, threshold=0.15):
        """Answer a question about 3D Max."""
        # Search for relevant Q&A pairs
        results = self.search(query, top_k=3, threshold=threshold)

        if not results:
            return (
                "Извините, я не нашел ответ на ваш вопрос в документации. "
                "Попробуйте переформулировать вопрос или обратитесь к руководству пользователя 3D Max."
            )

        # Return the best match
        best_match = results[0]

        # Check if it's a good match or a tentative match
        if best_match['similarity'] > 0.4:  # Adjusted threshold for "good" match
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