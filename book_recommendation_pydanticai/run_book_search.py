# run_book_search.py
import asyncio
from book_search_service import BookSearchService
from book_repository import BookRepository


async def main():
    """Test our book search service with a direct script."""
    print("Starting book search test...")

    # Initialize our services
    search_service = BookSearchService()
    repository = BookRepository()

    # Test with a well-known book
    book_title = "The Great Gatsby"
    print(f"Searching for information about '{book_title}'...")

    # Search for the book
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

        # Save to our repository
        print("\nSaving book to repository...")
        repository.add_book(book)
        print("Book saved successfully!")

        # Verify we can retrieve it
        retrieved_book = repository.find_book_by_title(book_title)
        if retrieved_book:
            print("\nSuccessfully retrieved book from repository:")
            print(f"Title: {retrieved_book.title}")
            print(f"Author: {retrieved_book.author}")
        else:
            print("\nError: Failed to retrieve book from repository")
    else:
        print("No book information found")


if __name__ == "__main__":
    # Run the async function
    asyncio.run(main())