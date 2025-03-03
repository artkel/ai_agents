from enum import Enum
from typing import List, Optional, Set
from pydantic import BaseModel, Field
from typing_extensions import TypedDict

# define enums for consistent categorization
class Genre(str, Enum):
    """Book genres as an enumeration for consistent categorization."""
    SCIENCE_FICTION = "science fiction"
    FANTASY = "fantasy"
    MYSTERY = "mystery"
    THRILLER = "thriller"
    ROMANCE = "romance"
    HISTORICAL = "historical"
    BIOGRAPHY = "biography"
    NON_FICTION = "non-fiction"
    HORROR = "horror"
    YOUNG_ADULT = "young adult"
    LITERARY = "literary fiction"

class Theme(str, Enum):
    """Common book themes for consistent categorization."""
    ADVENTURE = "adventure"
    COMING_OF_AGE = "coming of age"
    REDEMPTION = "redemption"
    SURVIVAL = "survival"
    LOVE = "love"
    LOSS = "loss"
    POWER = "power"
    IDENTITY = "identity"
    GOOD_VS_EVIL = "good vs evil"
    FRIENDSHIP = "friendship"

class Mood(str, Enum):
    """Emotional tones of books for consistent categorization."""
    UPLIFTING = "uplifting"
    DARK = "dark"
    HUMOROUS = "humorous"
    THOUGHTFUL = "thoughtful"
    SUSPENSEFUL = "suspenseful"
    ROMANTIC = "romantic"
    MELANCHOLIC = "melancholic"
    INSPIRING = "inspiring"

# define data models
class Book(BaseModel):
    """Model representing a book with its key attributes."""
    title: str = Field(description="Title of the book")
    author: str = Field(description="Author of the book")
    genres: List[Genre] = Field(description="Genres this book belongs to")
    year: Optional[int] = Field(None, description="Publication year")
    description: Optional[str] = Field(None, description="Brief description of the book")
    themes: List[Theme] = Field(default_factory=list, description="Key themes or topics in the book")
    mood: List[Mood] = Field(default_factory=list, description="Emotional tone of the book")

class RecommendationReason(BaseModel):
    """Explanation for why a book was recommended."""
    book_title: str = Field(description="Title of the recommended book")
    reason: str = Field(description="Explanation of why this book was recommended")
    similarity_score: int = Field(
        description="How similar this book is to the user's preferences on a scale of 1-10",
        ge=1, le=10
    )

class RecommendationResponse(BaseModel):
    """Response model containing book recommendations."""
    input_books: List[Book] = Field(description="The books the user provided as input")
    recommended_books: List[Book] = Field(description="List of recommended books")
    recommendation_reasons: List[RecommendationReason] = Field(
        description="Explanations for each recommendation"
    )


class UserPreferences(BaseModel):
    """Model representing a user's book preferences."""
    liked_books: List[Book] = Field(default_factory=list, description="Books the user has liked")
    favorite_genres: Set[Genre] = Field(default_factory=set, description="User's favorite genres")
    favorite_authors: Set[str] = Field(default_factory=set, description="User's favorite authors")
    favorite_themes: Set[Theme] = Field(default_factory=set, description="Themes the user enjoys")
    favorite_moods: Set[Mood] = Field(default_factory=set, description="Moods the user enjoys")

    def update_from_book(self, book: Book):
        """Update preferences based on a new liked book."""
        self.liked_books.append(book)
        for genre in book.genres:
            self.favorite_genres.add(genre)
        self.favorite_authors.add(book.author)
        for theme in book.themes:
            self.favorite_themes.add(theme)
        for mood in book.mood:
            self.favorite_moods.add(mood)