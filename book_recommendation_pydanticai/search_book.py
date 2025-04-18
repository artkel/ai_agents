# search_book.py
import json
import asyncio
from pathlib import Path

from book_search_service import BookSearchService
from book_repository import BookRepository


async def search_for_book(title):
    """Search for a specific book title."""
    search_service = BookSearchService()
    return await search_service.search_book_by_title(title)


def main():
    """Interactive book search tool."""
    book_repo = BookRepository("book_repository.json")

    # Get the title from user input
    title = input("Enter the book title you want to search for: ")

    print(f"\nSearching for: {title}")
    print("-" * 50)

    # Search for the book
    book = asyncio.run(search_for_book(title))

    if book:
        print("\nBook found!")
        print(f"Title: {book.title}")
        print(f"Author: {book.author}")
        print(f"Year: {book.year or 'Unknown'}")
        print(f"Genres: {', '.join(str(genre) for genre in book.genres)}")
        print(f"Themes: {', '.join(str(theme) for theme in book.themes)}")
        print(f"Mood: {', '.join(str(mood) for mood in book.mood)}")

        # Display literary style information
        if hasattr(book, 'literary_style') and book.literary_style:
            print(f"Literary Style: {', '.join(str(style) for style in book.literary_style)}")
        else:
            print("Literary Style: Not available")

        # Display rating information
        if book.avg_rating is not None:
            print(f"Average Rating: {book.avg_rating}/5 (from {book.ratings_count or 'unknown number of'} ratings)")
        else:
            print("Average Rating: Not available")

        # Print description (truncated if too long)
        if book.description:
            desc = book.description
            if len(desc) > 300:
                desc = desc[:300] + "..."
            print(f"\nDescription: {desc}")

        # Save to repository option
        save = input("\nSave this book to repository? (y/n): ").lower()
        if save == 'y':
            book_repo.add_book(book)
            print("Book added to repository.")

            # Show all books in repository
            all_books = book_repo.get_all_books()
            print(f"\nRepository now contains {len(all_books)} books:")
            for i, b in enumerate(all_books, 1):
                rating_info = f" ({b.avg_rating}/5)" if b.avg_rating is not None else ""
                print(f"{i}. {b.title} by {b.author}{rating_info}")

        # Save full details to a JSON file option
        save_json = input("\nSave full details to JSON file? (y/n): ").lower()
        if save_json == 'y':
            # Convert to dict and handle Enum serialization
            book_dict = book.dict()
            book_dict["genres"] = [str(genre) for genre in book.genres]
            book_dict["themes"] = [str(theme) for theme in book.themes]
            book_dict["mood"] = [str(mood) for mood in book.mood]

            # Handle literary style serialization if it exists
            if hasattr(book, 'literary_style') and book.literary_style:
                book_dict["literary_style"] = [str(style) for style in book.literary_style]

            # Create a filename from the book title
            filename = f"{title.replace(' ', '_').lower()}_info.json"
            Path(filename).write_text(json.dumps(book_dict, indent=2))
            print(f"Book details saved to {filename}")
    else:
        print("No information found for this title.")

    # Ask if user wants to search for another book
    another = input("\nSearch for another book? (y/n): ").lower()
    if another == 'y':
        main()


if __name__ == "__main__":
    main()