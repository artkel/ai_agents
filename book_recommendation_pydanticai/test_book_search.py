# run_book_search_test.py
import asyncio
from book_search_service import BookSearchService


async def main():
    """Test our book search service."""
    search_service = BookSearchService()

    # Test with a well-known book
    book_title = "The Great Gatsby"
    print(f"Searching for information about '{book_title}'...")

    book = await search_service.search_book_by_title(book_title)

    # Print what we found
    if book:
        print("\nBook information found:")
        print(f"Title: {book.title}")
        print(f"Author: {book.author}")
        print(f"Year: {book.year}")
        print(f"Genres: {[g for g in book.genres]}")
        print(f"Themes: {[t for t in book.themes]}")
        print(f"Mood: {[m for m in book.mood]}")
        print(f"Description: {book.description}")

        # Also save to our repository
        print("\nSaving book to repository...")
        from book_repository import BookRepository
        repo = BookRepository()
        repo.add_book(book)
        print("Book saved successfully!")
    else:
        print("No book information found")


if __name__ == "__main__":
    asyncio.run(main())