from book_repository import BookRepository
from models import Book, Genre, Theme, Mood
from typing_extensions import TypedDict

def test_repository_operations():
    """Test basic repository operations."""
    # Use a test-specific file
    repo = BookRepository("test_repository.json")

    # Create a test book
    test_book = Book(
        title="Test Book",
        author="Test Author",
        genres=[Genre.SCIENCE_FICTION],
        themes=[Theme.ADVENTURE],
        mood=[Mood.SUSPENSEFUL]
    )

    # Add the book
    repo.add_book(test_book)

    # Find the book
    found_book = repo.find_book_by_title("Test Book")
    assert found_book is not None
    assert found_book.title == "Test Book"
    assert found_book.author == "Test Author"
    assert Genre.SCIENCE_FICTION in found_book.genres

    # Verify case insensitivity
    found_book_case_insensitive = repo.find_book_by_title("test book")
    assert found_book_case_insensitive is not None

    # Try finding a non-existent book
    not_found = repo.find_book_by_title("Non-existent Book")
    assert not_found is None

    print("✅ Repository tests passed!")


if __name__ == "__main__":
    test_repository_operations()