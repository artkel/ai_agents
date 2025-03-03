# test_models.py
from typing_extensions import TypedDict
from models import Book, Genre, Theme, Mood, RecommendationReason, RecommendationResponse, UserPreferences
from pydantic import ValidationError
import pytest


def test_book_creation():
    """Test that we can create valid Book instances."""
    # Create a valid book
    book = Book(
        title="Project Hail Mary",
        author="Andy Weir",
        genres=[Genre.SCIENCE_FICTION],
        themes=[Theme.ADVENTURE, Theme.SURVIVAL],
        mood=[Mood.SUSPENSEFUL, Mood.INSPIRING]
    )

    # Check that fields were set correctly
    assert book.title == "Project Hail Mary"
    assert book.author == "Andy Weir"
    assert book.genres == [Genre.SCIENCE_FICTION]
    assert Theme.ADVENTURE in book.themes
    assert Mood.INSPIRING in book.mood

    print("✅ Book creation test passed")


def test_book_validation():
    """Test that validation catches invalid Book instances."""
    try:
        # Try to create a book with an invalid genre
        Book(
            title="Invalid Book",
            author="Test Author",
            genres=["not a valid genre"]  # This should fail validation
        )
        assert False, "Validation should have failed"
    except ValidationError as e:
        # Validation correctly failed
        assert "genres" in str(e)
        print("✅ Book validation test passed")


def test_user_preferences_update():
    """Test that UserPreferences updates correctly when a book is added."""
    # Create a user preference object
    prefs = UserPreferences()
    assert len(prefs.liked_books) == 0

    # Add a book
    book = Book(
        title="Dune",
        author="Frank Herbert",
        genres=[Genre.SCIENCE_FICTION, Genre.FANTASY],
        themes=[Theme.POWER, Theme.IDENTITY, Theme.ADVENTURE],
        mood=[Mood.THOUGHTFUL, Mood.SUSPENSEFUL]
    )

    # Update preferences
    prefs.update_from_book(book)

    # Check that preferences were updated
    assert len(prefs.liked_books) == 1
    assert Genre.SCIENCE_FICTION in prefs.favorite_genres
    assert "Frank Herbert" in prefs.favorite_authors
    assert Theme.POWER in prefs.favorite_themes
    assert Mood.THOUGHTFUL in prefs.favorite_moods

    print("✅ UserPreferences update test passed")


def test_recommendation_response():
    """Test creation of a recommendation response."""
    # Create input books
    book1 = Book(
        title="The Hobbit",
        author="J.R.R. Tolkien",
        genres=[Genre.FANTASY],
        themes=[Theme.ADVENTURE],
        mood=[Mood.INSPIRING]
    )

    book2 = Book(
        title="Game of Thrones",
        author="George R.R. Martin",
        genres=[Genre.FANTASY],
        themes=[Theme.POWER, Theme.GOOD_VS_EVIL],
        mood=[Mood.DARK]
    )

    # Create recommended book
    rec_book = Book(
        title="The Name of the Wind",
        author="Patrick Rothfuss",
        genres=[Genre.FANTASY],
        themes=[Theme.COMING_OF_AGE, Theme.ADVENTURE],
        mood=[Mood.THOUGHTFUL, Mood.INSPIRING]
    )

    # Create recommendation reason
    reason = RecommendationReason(
        book_title="The Name of the Wind",
        reason="Similar fantasy setting with an epic adventure narrative",
        similarity_score=8
    )

    # Create recommendation response
    response = RecommendationResponse(
        input_books=[book1, book2],
        recommended_books=[rec_book],
        recommendation_reasons=[reason]
    )

    # Check that response was created correctly
    assert len(response.input_books) == 2
    assert len(response.recommended_books) == 1
    assert response.recommendation_reasons[0].similarity_score == 8

    print("✅ RecommendationResponse test passed")


if __name__ == "__main__":
    # Run tests
    test_book_creation()
    test_book_validation()
    test_user_preferences_update()
    test_recommendation_response()
    print("All tests passed!")