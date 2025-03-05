# book_search_service.py (updated with Google Books API and rating information)
import os
import re
from typing import List, Optional
import httpx
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

from models import Book, Genre, Theme, Mood

# Load environment variables from .env file
load_dotenv()


class BookSearchService:
    """Service for searching book information using Google Books API and OpenAI."""

    def __init__(self):
        """Initialize the book search service with OpenAI model."""
        # Get API key from environment
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key is required. Please set the OPENAI_API_KEY environment variable.")

        # Create an OpenAI model with the API key
        openai_model = OpenAIModel(
            "gpt-4o",  # "gpt-3.5-turbo-0125",
            api_key=api_key
        )

        # Extraction agent to process additional book information
        self.extraction_agent = Agent(
            model=openai_model,
            result_type=Book,
            system_prompt=(
                "You are a book information extraction specialist. Your task is to extract structured "
                "information about books from the provided details. Focus on determining accurate "
                "genres, themes, emotional tone/mood, and including any provided rating data.\n\n"

                "For genres, use only these categories: science fiction, fantasy, mystery, thriller, "
                "romance, historical, biography, non-fiction, horror, young adult, literary fiction.\n\n"

                "For themes, identify concepts like: adventure, coming of age, redemption, survival, love, "
                "loss, power, identity, good vs evil, friendship.\n\n"

                "For mood, identify emotional tones like: uplifting, dark, humorous, thoughtful, "
                "suspenseful, romantic, melancholic, inspiring.\n\n"

                "Also include average rating (0-5 scale) and ratings count when available from Google Books data."
            )
        )

    async def search_book_by_title(self, title: str) -> Optional[Book]:
        """
        Search for information about a book by its title, using both Google Books API
        and the model's existing knowledge.
        """
        try:
            # Step 1: Get data from Google Books API
            query = f"intitle:{title}"
            url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=10"

            print(f"Searching Google Books API for: {title}")

            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()

            # Check if we got any results
            if 'items' not in data or not data['items']:
                print(f"No Google Books results found for {title}")
                google_books_data = None
            else:
                book_match = self._find_best_book_match(data['items'], title)
                if book_match:
                    google_books_data = book_match['volumeInfo']
                else:
                    google_books_data = None

            # Step 2: Use the extraction agent with a prompt that encourages using both
            # Google Books data AND its own knowledge
            prompt = f"""
            Task: Extract comprehensive, accurate information about "{title}" for our book recommendation system.

            Google Books Data:
            """

            if google_books_data:
                author = google_books_data.get('authors', ['Unknown'])[
                    0] if 'authors' in google_books_data else 'Unknown'

                # Extract year
                year = None
                if 'publishedDate' in google_books_data:
                    year_match = re.search(r'(\d{4})', google_books_data['publishedDate'])
                    if year_match:
                        year = int(year_match.group(1))

                # Extract rating information
                avg_rating = None
                ratings_count = None
                if 'averageRating' in google_books_data:
                    avg_rating = google_books_data['averageRating']
                if 'ratingsCount' in google_books_data:
                    ratings_count = google_books_data['ratingsCount']

                # Add Google Books data to prompt
                prompt += f"""
                Title: {google_books_data.get('title', title)}
                Author: {author}
                Year: {year if year else "Unknown"}
                Categories: {', '.join(google_books_data.get('categories', []))}
                Average Rating: {avg_rating if avg_rating is not None else "Not available"} (out of 5)
                Ratings Count: {ratings_count if ratings_count is not None else "Not available"}
                Description: {google_books_data.get('description', 'Not available')}
                """
            else:
                prompt += "No detailed information found in Google Books API.\n"

            prompt += f"""
            Your Task: 
            1. For well-known books, use your own knowledge to provide accurate information about genre, themes, mood, and original publication year.
            2. For newer or obscure books, rely primarily on the Google Books data.
            3. Always create a complete Book object with all required fields.

            For "{title}", please provide:
            - Accurate author name
            - Original publication year (not recent edition)
            - Appropriate genres from our supported list
            - 2-4 major themes present in the book
            - 1-2 predominant mood elements
            - Include the average rating and ratings count if available from Google Books data

            Note: If this is a well-known classic, please use your knowledge of literature to provide accurate information even if the Google Books data is incomplete. However, for rating data, always use the Google Books information if available.
            """

            # Use the extraction agent to create a Book object
            extraction_result = await self.extraction_agent.run(prompt)
            return extraction_result.data

        except Exception as e:
            print(f"Error searching for book '{title}': {e}")
            return None

    def _find_best_book_match(self, items, search_title):
        """
        Find the best matching book from the search results.

        Args:
            items: List of book items from the Google Books API
            search_title: The title that was searched for

        Returns:
            The best matching book item, or None if no good match is found
        """
        search_title_lower = search_title.lower()

        # Score each book based on relevance criteria
        scored_items = []
        for item in items:
            score = 0
            info = item.get('volumeInfo', {})

            # Check title match (case insensitive)
            title = info.get('title', '')
            if title.lower() == search_title_lower:
                score += 100  # Exact match gets highest priority
            elif search_title_lower in title.lower():
                score += 50  # Partial match

            # Prefer items with more complete information
            if 'description' in info and len(info['description']) > 100:
                score += 30  # Good description
            if 'authors' in info:
                score += 10  # Has author information
            if 'categories' in info:
                score += 10  # Has category information
            if 'publishedDate' in info:
                score += 10  # Has publication date

                # Prefer original/earlier editions for classics
                try:
                    year = int(re.search(r'(\d{4})', info['publishedDate']).group(1))
                    if year < 2000:  # Arbitrary cutoff for "older" editions
                        score += (2000 - year) / 100  # Earlier works get slightly higher scores
                except (AttributeError, ValueError):
                    pass

            # Prefer items with rating information
            if 'averageRating' in info:
                score += 15  # Has rating information
            if 'ratingsCount' in info and info['ratingsCount'] > 10:
                score += 10  # Has a meaningful number of ratings

            # Avoid derivative works (poems from books, study guides, etc.)
            subtitle = info.get('subtitle', '')
            if subtitle and ('poems' in subtitle.lower() or 'chapter' in subtitle.lower()
                             or 'guide' in subtitle.lower() or 'analysis' in subtitle.lower()):
                score -= 50  # Probably not the main book

            # Score based on page count - prefer full books
            if 'pageCount' in info and info['pageCount'] > 100:
                score += 10  # Likely a full book, not a short excerpt

            scored_items.append((score, item))

        # Sort by score (highest first) and return the best match
        scored_items.sort(reverse=True, key=lambda x: x[0])
        return scored_items[0][1] if scored_items else None

    def _map_categories_to_genres(self, categories):
        """
        Map Google Books categories to our Genre enum values.

        Args:
            categories: List of category strings from Google Books API

        Returns:
            List of Genre enum values
        """
        genres = []

        # Direct mapping of common Google Books categories to our genres
        category_mapping = {
            'FICTION': Genre.FICTION,
            'SCIENCE FICTION': Genre.SCIENCE_FICTION,
            'FANTASY': Genre.FANTASY,
            'MYSTERY': Genre.MYSTERY,
            'THRILLER': Genre.THRILLER,
            'ROMANCE': Genre.ROMANCE,
            'HISTORICAL FICTION': Genre.HISTORICAL,
            'HISTORY': Genre.HISTORY,
            'BIOGRAPHY & AUTOBIOGRAPHY': Genre.BIOGRAPHY,
            'HORROR': Genre.HORROR,
            'YOUNG ADULT FICTION': Genre.YOUNG_ADULT,
            'JUVENILE FICTION': Genre.JUVENILE,
            'LITERARY CRITICISM': Genre.LITERARY,
            'LITERARY COLLECTIONS': Genre.LITERARY,
            'POETRY': Genre.POETRY,
            'DRAMA': Genre.DRAMA,
            'PHILOSOPHY': Genre.PHILOSOPHY,
            'SCIENCE': Genre.SCIENCE,
            'BUSINESS & ECONOMICS': Genre.BUSINESS,
            'TRAVEL': Genre.TRAVEL,
            'TRUE CRIME': Genre.TRUE_CRIME,
            'COMICS & GRAPHIC NOVELS': Genre.COMICS
        }

        # Process each category
        for category in categories:
            # Normalize to uppercase for matching
            category_upper = category.upper()

            # Check for direct matches first
            if category_upper in category_mapping:
                genres.append(category_mapping[category_upper])
            # Check for partial matches
            else:
                for key, genre in category_mapping.items():
                    if key in category_upper or category_upper in key:
                        genres.append(genre)
                        break

        # If no genres were matched, default to FICTION for fiction books
        # or NON_FICTION for everything else
        if not genres and categories:
            if 'FICTION' in categories[0].upper():
                genres.append(Genre.FICTION)
            else:
                genres.append(Genre.NON_FICTION)

        # Remove duplicates while preserving order
        return list(dict.fromkeys(genres))