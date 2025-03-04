# ============================
# book_repository.py
import json
import os
from typing import List, Optional
from pathlib import Path
from typing_extensions import TypedDict

from models import Book, Genre, Theme, Mood


class BookRepository:
    """Repository for storing and retrieving book information."""

    def __init__(self, file_path: str = "book_repository.json"):
        """
        Initialize the book repository.

        Args:
            file_path: Path to the JSON file where books will be stored
        """
        self.file_path = Path(file_path)
        self._ensure_repository_exists()

    def _ensure_repository_exists(self) -> None:
        """Create the repository file if it doesn't exist."""
        if not self.file_path.exists():
            # Initialize with an empty books array
            self.file_path.write_text(json.dumps({"books": []}))

    def get_all_books(self) -> List[Book]:
        """Retrieve all books from the repository."""
        data = self._read_repository()
        # Convert the raw data to Book objects
        return [Book.parse_obj(book_data) for book_data in data["books"]]

    def find_book_by_title(self, title: str) -> Optional[Book]:
        """
        Find a book by its title.

        Args:
            title: The title to search for (case-insensitive)

        Returns:
            The Book object if found, None otherwise
        """
        books = self.get_all_books()
        # Perform case-insensitive search
        for book in books:
            if book.title.lower() == title.lower():
                return book
        return None

    def add_book(self, book: Book) -> None:
        """
        Add a new book to the repository.

        Args:
            book: The Book object to add
        """
        data = self._read_repository()
        # Check if book already exists
        existing_books = [b for b in data["books"]
                          if b.get("title", "").lower() == book.title.lower()]

        if not existing_books:
            # Convert Pydantic model to dict for JSON serialization
            data["books"].append(book.dict())
            self._write_repository(data)

    def _read_repository(self) -> dict:
        """Read the repository file and return its contents."""
        return json.loads(self.file_path.read_text())

    def _write_repository(self, data: dict) -> None:
        """Write data to the repository file."""
        self.file_path.write_text(json.dumps(data, indent=2))