import asyncio
import json
from pathlib import Path

from book_repository import BookRepository
from models import UserPreferences, RecommendationResponse
from recommendation_service import RecommendationService


async def main():
    """Generate book recommendations based on books in the repository."""
    # Load books from repository
    repo = BookRepository("book_repository.json")
    all_books = repo.get_all_books()

    if not all_books:
        print("No books found in repository. Please add some books first using the search_book.py script.")
        return

    print(f"Found {len(all_books)} books in your repository:")
    for i, book in enumerate(all_books, 1):
        print(f"{i}. {book.title} by {book.author}")

    # Create user preferences object with all books in the repository
    preferences = UserPreferences()
    for book in all_books:
        preferences.update_from_book(book)

    print("\nAnalyzing your reading preferences...")

    # Initialize recommendation service
    service = RecommendationService()

    # Get number of recommendations from user
    try:
        num_recommendations = int(input("\nHow many recommendations would you like? (1-10): "))
        num_recommendations = max(1, min(num_recommendations, 10))  # Ensure between 1 and 10
    except ValueError:
        print("Invalid input, using default of 5 recommendations.")
        num_recommendations = 5

    print(f"\nGenerating {num_recommendations} personalized recommendations...")

    # Get recommendations
    try:
        result = await service.get_recommendations(preferences, num_recommendations)
        display_recommendations(result)

        # Save recommendations to file
        save = input("\nSave recommendations to file? (y/n): ").lower()
        if save == 'y':
            save_recommendations(result)

    except Exception as e:
        print(f"Error generating recommendations: {e}")


def display_recommendations(result: RecommendationResponse):
    """Display the recommendations in a readable format."""
    if not result.recommended_books:
        print("\nNo recommendations could be generated. Try adding more diverse books to your repository.")
        return

    print("\n===== BOOK RECOMMENDATIONS =====\n")

    for i, (book, reason) in enumerate(zip(result.recommended_books, result.recommendation_reasons), 1):
        print(f"RECOMMENDATION #{i}: {book.title}")
        print(f"Author: {book.author}")
        print(f"Year: {book.year or 'Unknown'}")
        print(f"Genres: {', '.join(str(genre) for genre in book.genres)}")

        # Display literary style if available
        if hasattr(book, 'literary_style') and book.literary_style:
            print(f"Literary Style: {', '.join(str(style) for style in book.literary_style)}")

        # Display rating if available
        if book.avg_rating is not None:
            print(f"Average Rating: {book.avg_rating}/5 (from {book.ratings_count or 'unknown number of'} ratings)")

        # Display recommendation reason
        print(f"Similarity Score: {reason.similarity_score}/10")
        print(f"Why Recommended: {reason.reason}")

        # Display description (truncated if too long)
        if book.description:
            desc = book.description
            if len(desc) > 200:
                desc = desc[:200] + "..."
            print(f"Description: {desc}")

        print("-" * 60)


def save_recommendations(result: RecommendationResponse):
    """Save recommendations to a JSON file."""
    # Create a serializable version of the recommendation response
    serializable_result = {
        "input_books": [book.title for book in result.input_books],
        "recommendations": []
    }

    for book, reason in zip(result.recommended_books, result.recommendation_reasons):
        # Convert book to dict and handle Enum serialization
        book_dict = book.dict()
        book_dict["genres"] = [str(genre) for genre in book.genres]
        book_dict["themes"] = [str(theme) for theme in book.themes]
        book_dict["mood"] = [str(mood) for mood in book.mood]

        # Handle literary style serialization if it exists
        if hasattr(book, 'literary_style') and book.literary_style:
            book_dict["literary_style"] = [str(style) for style in book.literary_style]

        # Add recommendation reason
        book_dict["reason"] = reason.reason
        book_dict["similarity_score"] = reason.similarity_score

        serializable_result["recommendations"].append(book_dict)

    # Save to file
    filepath = Path("book_recommendations.json")
    filepath.write_text(json.dumps(serializable_result, indent=2))
    print(f"Recommendations saved to {filepath}")


if __name__ == "__main__":
    asyncio.run(main())