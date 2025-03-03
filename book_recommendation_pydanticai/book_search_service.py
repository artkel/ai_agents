# book_search_service.py
import asyncio
import os
from typing import List, Optional
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.anthropic import AnthropicModel

from models import Book, Genre, Theme, Mood

# Load environment variables from .env file
load_dotenv()


class BookSearchService:
    """Service for searching book information online using Claude."""

    def __init__(self):
        """Initialize the book search service with Claude model."""
        # Get API key from environment
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("Anthropic API key is required. Please set the ANTHROPIC_API_KEY environment variable.")

        # Create an AnthropicModel with the API key
        claude_model = AnthropicModel(
            "claude-3-haiku-20240307",
            api_key=api_key
        )

        # Extraction agent to process search results into structured book information
        self.extraction_agent = Agent(
            model=claude_model,  # Use the configured model instance
            result_type=Book,
            system_prompt=(
                "You are a book information extraction specialist. Your task is to extract structured "
                "information about books from search results. Extract as much information as possible "
                "about the title, author, genre, publication year, description, themes, and mood.\n\n"

                "For genres, use only these categories: science fiction, fantasy, mystery, thriller, "
                "romance, historical, biography, non-fiction, horror, young adult, literary fiction.\n\n"

                "For themes, identify concepts like: adventure, coming of age, redemption, survival, love, "
                "loss, power, identity, good vs evil, friendship.\n\n"

                "For mood, identify emotional tones like: uplifting, dark, humorous, thoughtful, "
                "suspenseful, romantic, melancholic, inspiring."
            )
        )

    async def perform_web_search(self, query: str) -> str:
        """
        Mock web search that returns predefined information for testing purposes.
        In a real implementation, this would make an actual web search request.
        """
        if "The Great Gatsby" in query:
            return """
            Title: The Great Gatsby - Wikipedia
            Snippet: The Great Gatsby is a 1925 novel by American writer F. Scott Fitzgerald. Set in the Jazz Age on Long Island, near New York City, the novel depicts first-person narrator Nick Carraway's interactions with mysterious millionaire Jay Gatsby and Gatsby's obsession to reunite with his former lover, Daisy Buchanan.
            Link: https://en.wikipedia.org/wiki/The_Great_Gatsby

            Title: The Great Gatsby by F. Scott Fitzgerald - Goodreads
            Snippet: The Great Gatsby, F. Scott Fitzgerald's third book, stands as the supreme achievement of his career. First published in 1925, this quintessential novel of the Jazz Age has been acclaimed by generations of readers. The story of the fabulously wealthy Jay Gatsby and his love for the beautiful Daisy Buchanan, of lavish parties on Long Island at a time when The New York Times noted "gin was the national drink and sex the national obsession," it is an exquisitely crafted tale of America in the 1920s.
            Link: https://www.goodreads.com/book/show/4671.The_Great_Gatsby

            Title: The Great Gatsby (Book) - Themes, Analysis & Summary
            Snippet: The Great Gatsby explores themes of decadence, idealism, social upheaval, resistance to change, and excess. The story primarily concerns the young and mysterious millionaire Jay Gatsby and his quixotic passion and obsession with the beautiful former debutante Daisy Buchanan. The novel has been described as a cautionary tale regarding the American Dream.
            Link: https://www.sparknotes.com/lit/gatsby/
            """
        else:
            return f"Information about the book '{query}' could not be found in sufficient detail."

    async def search_book_by_title(self, title: str) -> Optional[Book]:
        """
        Search for information about a book by its title.

        Args:
            title: The title of the book to search for

        Returns:
            A Book object with the information found, or None if no information could be found
        """
        try:
            # Search for information about the book
            search_query = f"book {title} author genre plot summary year published"
            search_text = await self.perform_web_search(search_query)

            # Extract structured information from the search results
            extraction_result = await self.extraction_agent.run(
                f"Extract information about '{title}' from these search results:\n\n{search_text}"
            )

            return extraction_result.data
        except Exception as e:
            print(f"Error searching for book '{title}': {e}")
            return None