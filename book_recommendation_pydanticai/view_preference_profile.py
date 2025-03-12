# test_preference_profile.py
import asyncio
import json
from pathlib import Path
from typing import List, Dict, Any

from book_repository import BookRepository
from models import UserPreferences, Book

# Import the profile building functions we created
from user_preference_profile import (
    analyze_genre_preferences,
    analyze_author_preferences,
    analyze_mood_preferences,
    analyze_theme_patterns,
    analyze_literary_style_preferences,
    build_user_preference_profile,
    get_era
)


def pretty_print_profile(profile: Dict[str, Any]) -> None:
    """Print the user preference profile in a readable format."""
    print("\n===== USER PREFERENCE PROFILE =====\n")

    # Print top preferences summary
    # [All your existing print code remains the same]

    # Export the profile to a JSON file for further inspection
    profile_path = Path("user_preference_profile.json")

    # Create a serializable copy of the profile
    serializable_profile = {}

    # Process each section of the profile
    for section_key, section_data in profile.items():
        if section_key == "top_preferences":
            # Handle top preferences specially
            serializable_profile[section_key] = {
                k: [list(item) for item in v] if isinstance(v, list) else str(v)
                for k, v in section_data.items()
            }
        else:
            # Handle each analysis section
            serializable_section = {}
            for key, value in section_data.items():
                if key in ("co_occurrences", "genre_correlations", "era_correlations"):
                    # Convert dictionary with tuple keys to a list of triplets [key1, key2, value]
                    serializable_section[key] = [
                        [str(k[0]), str(k[1]), v] for k, v in value.items()
                    ]
                else:
                    # For simple dictionaries, convert non-string keys to strings
                    serializable_section[key] = {
                        str(k): v for k, v in value.items()
                    }
            serializable_profile[section_key] = serializable_section

    profile_path.write_text(json.dumps(serializable_profile, indent=2))
    print(f"\nProfile exported to {profile_path}")


def main():
    """Load books from repository and build a user preference profile."""
    # Load books from repository
    repo = BookRepository("book_repository.json")
    all_books = repo.get_all_books()

    print(f"Loaded {len(all_books)} books from repository.")

    if not all_books:
        print("No books found in repository. Please add some books first.")
        return

    # Print the titles of books found
    print("\nBooks in repository:")
    for i, book in enumerate(all_books, 1):
        print(f"{i}. {book.title} by {book.author}")

    # Create a user preferences object with all books
    preferences = UserPreferences()
    for book in all_books:
        preferences.update_from_book(book)

    # Build and print the preference profile
    profile = build_user_preference_profile(preferences)
    pretty_print_profile(profile)


if __name__ == "__main__":
    main()