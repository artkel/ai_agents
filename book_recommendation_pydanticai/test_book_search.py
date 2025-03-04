# test_book_search.py
import pytest
import asyncio
from book_search_service import BookSearchService
from book_repository import BookRepository
from pydantic_ai import capture_run_messages
import time


@pytest.mark.asyncio
async def test_search_and_save_books():
    """Test searching for books and saving them to the repository."""
    book_titles = [
        "Dark Avenues",
        "Misery",
        "Anna Karenina",
        "Kim"
    ]

    search_service = BookSearchService()
    book_repo = BookRepository("book_repository.json")

    from pydantic_ai import capture_run_messages

    for title in book_titles:
        print(f"\n{'=' * 60}")
        print(f"SEARCHING FOR: {title}")
        print(f"{'=' * 60}")

        if title != book_titles[0]:
            print("Waiting 15 seconds to avoid rate limiting...")
            time.sleep(15)

        # First, let's capture what the search agent returns
        search_result = await search_service.search_agent.run(
            f"Find detailed information about the book '{title}'. "
            f"Include the author, publication year, genre, plot summary, themes, and critical reception."
        )

        print(f"\n--- SEARCH RESULTS FOR '{title}' ---")
        # Print the first 500 characters to see a sample of what was found
        search_text = search_result.data
        print(search_text[:500] + "..." if len(search_text) > 500 else search_text)

        # Now proceed with the regular search and extraction
        with capture_run_messages() as messages:
            book = await search_service.search_book_by_title(title)

            # Check tool usage
            tool_used = False
            for msg in messages:
                if hasattr(msg, 'parts'):
                    for part in msg.parts:
                        if hasattr(part, 'tool_name') and part.tool_name == 'duckduckgo_search':
                            tool_used = True
                            print(f"✓ DuckDuckGo search tool was used for '{title}'")
                            break

            if not tool_used:
                print(f"⚠ WARNING: DuckDuckGo search tool was NOT used for '{title}'!")

        if book:
            print(f"\nFound: {book.title} by {book.author}")
            print(f"Genres: {', '.join(str(genre) for genre in book.genres)}")
            book_repo.add_book(book)
            print(f"Added to book repository")
        else:
            print(f"\nNo information found for {title}")

    # Print repository summary
    all_books = book_repo.get_all_books()
    print(f"\nRepository now contains {len(all_books)} books:")
    for i, book in enumerate(all_books, 1):
        print(f"{i}. {book.title} by {book.author}")