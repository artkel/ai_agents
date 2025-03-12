from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from typing import List
import os
import json
from user_preference_profile import build_user_preference_profile
from book_search_service import BookSearchService
from models import UserPreferences, Book, RecommendationResponse, RecommendationReason


class RecommendationService:
    """Service for generating personalized book recommendations."""

    def __init__(self):
        """Initialize the recommendation service with OpenAI model."""
        # Get API key from environment
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key is required. Please set the OPENAI_API_KEY environment variable.")

        # Create an OpenAI model with the API key
        openai_model = OpenAIModel(
            "o3-mini",  # or "gpt-4o" for better recommendations
            api_key=api_key
        )

        # Define the recommendation agent that will suggest books
        self.recommendation_agent = Agent(
            model=openai_model,
            result_type=List[str],
            model_settings={"reasoning_effort": "medium"},
            system_prompt=(
                "You are a literary recommendation specialist with deep knowledge of books across all genres and time periods. "
                "Your task is to recommend books based on a detailed analysis of a user's reading preferences. "
                "Provide recommendations that match the user's taste profile while offering some diversity and discovery. "
                "Focus on suggesting books that are highly regarded, but not extremely obscure or difficult to find. "
                "Return your recommendations as a list of specific book titles that the user is likely to enjoy."
            )
        )

        # Book search service for enriching recommendations
        self.book_search_service = BookSearchService()

    async def generate_recommendations(self, preferences: UserPreferences, num_recommendations: int = 5) -> List[Book]:
        """
        Generate personalized book recommendations based on user preferences.

        Args:
            preferences: The user's reading preferences
            num_recommendations: Number of recommendations to generate

        Returns:
            List of recommended Book objects
        """
        # Build user preference profile
        profile = build_user_preference_profile(preferences)

        # Convert to a format suitable for the prompt
        profile_str = self._format_profile_for_prompt(profile)

        # Generate book title suggestions using GPT
        prompt = f"""
        I need personalized book recommendations based on the following user profile:

        {profile_str}

        Please suggest {num_recommendations + 2} books (title and author) that this person would likely enjoy 
        but hasn't read yet. Focus on matching their genre, theme, mood, and literary style preferences.
        Each recommendation should be distinct from books they've already read but share important characteristics.

        For each recommendation, briefly explain why it matches their preferences.
        Return ONLY a list of book titles without explanations, one title per line.
        """

        result = await self.recommendation_agent.run(prompt)
        suggested_titles = result.data

        # Ensure we have the requested number of recommendations (if available)
        suggested_titles = suggested_titles[:num_recommendations + 2]

        # Fetch detailed information for each suggested book
        recommendations = []
        for title in suggested_titles:
            book = await self.book_search_service.search_book_by_title(title)
            if book:
                # Check if this book is already in the user's liked books
                if not any(b.title.lower() == book.title.lower() for b in preferences.liked_books):
                    recommendations.append(book)
                    # Stop once we have enough recommendations
                    if len(recommendations) >= num_recommendations:
                        break

        return recommendations

    def _format_profile_for_prompt(self, profile: dict) -> str:
        """Format the user profile into a readable string for the prompt."""
        formatted = "USER READING PROFILE:\n\n"

        # Add books they've read
        if profile.get("read_books"):
            formatted += "Books they've read:\n"
            for book in profile.get("read_books", []):
                formatted += f"- {book}\n"
            formatted += "\n"

        # Add top preferences
        top = profile.get("top_preferences", {})

        if top.get("top_genres"):
            formatted += "Favorite Genres:\n"
            for genre, count in top["top_genres"]:
                formatted += f"- {genre} ({count} books)\n"
            formatted += "\n"

        if top.get("top_themes"):
            formatted += "Preferred Themes:\n"
            for theme, count in top["top_themes"]:
                formatted += f"- {theme} ({count} books)\n"
            formatted += "\n"

        if top.get("top_moods"):
            formatted += "Preferred Moods:\n"
            for mood, count in top["top_moods"]:
                formatted += f"- {mood} ({count} books)\n"
            formatted += "\n"

        if top.get("top_literary_styles"):
            formatted += "Preferred Literary Styles:\n"
            for style, count in top["top_literary_styles"]:
                formatted += f"- {style} ({count} books)\n"
            formatted += "\n"

        if top.get("favorite_authors"):
            formatted += "Favorite Authors:\n"
            for author in top["favorite_authors"]:
                formatted += f"- {author}\n"
            formatted += "\n"

        return formatted

    async def generate_recommendation_reasons(
            self,
            preferences: UserPreferences,
            recommendations: List[Book]
    ) -> List[RecommendationReason]:
        """
        Generate explanations for why each book was recommended.

        Args:
            preferences: The user's reading preferences
            recommendations: List of recommended books

        Returns:
            List of RecommendationReason objects
        """
        reasons = []
        profile = build_user_preference_profile(preferences)

        for book in recommendations:
            # Calculate a similarity score based on matching attributes
            similarity_score = self._calculate_similarity_score(profile, book)

            # Generate an explanation
            explanation = await self._generate_explanation(preferences, profile, book)

            reason = RecommendationReason(
                book_title=book.title,
                reason=explanation,
                similarity_score=similarity_score
            )
            reasons.append(reason)

        return reasons

    def _calculate_similarity_score(self, profile: dict, book: Book) -> int:
        """
        Calculate a similarity score between user preferences and a book.
        Returns a score from 1-10.
        """
        score = 0
        top_prefs = profile.get("top_preferences", {})

        # Genre match
        user_genres = {genre for genre, _ in top_prefs.get("top_genres", [])}
        if any(genre in user_genres for genre in book.genres):
            score += 3

        # Theme match
        user_themes = {theme for theme, _ in top_prefs.get("top_themes", [])}
        if any(theme in user_themes for theme in book.themes):
            score += 2

        # Mood match
        user_moods = {mood for mood, _ in top_prefs.get("top_moods", [])}
        if any(mood in user_moods for mood in book.mood):
            score += 2

        # Literary style match
        user_styles = {style for style, _ in top_prefs.get("top_literary_styles", [])}
        if hasattr(book, 'literary_style') and any(style in user_styles for style in book.literary_style):
            score += 2

        # Author match
        if book.author in profile.get("authors", {}).get("counts", {}):
            score += 1

        # Ensure the score is between 1 and 10
        return max(1, min(score, 10))

    async def _generate_explanation(
            self,
            preferences: UserPreferences,
            profile: dict,
            book: Book
    ) -> str:
        """Generate a personalized explanation for why this book was recommended."""
        # Extract key matching points
        matching_points = []

        # Check for genre matches
        user_genres = {genre for genre, _ in profile.get("top_preferences", {}).get("top_genres", [])}
        matching_genres = [genre for genre in book.genres if genre in user_genres]
        if matching_genres:
            matching_points.append(f"genre ({', '.join(str(g) for g in matching_genres)})")

        # Check for theme matches
        user_themes = {theme for theme, _ in profile.get("top_preferences", {}).get("top_themes", [])}
        matching_themes = [theme for theme in book.themes if theme in user_themes]
        if matching_themes:
            matching_points.append(f"theme ({', '.join(str(t) for t in matching_themes)})")

        # Check for mood matches
        user_moods = {mood for mood, _ in profile.get("top_preferences", {}).get("top_moods", [])}
        matching_moods = [mood for mood in book.mood if mood in user_moods]
        if matching_moods:
            matching_points.append(f"mood ({', '.join(str(m) for m in matching_moods)})")

        # Check for literary style matches
        if hasattr(book, 'literary_style'):
            user_styles = {style for style, _ in profile.get("top_preferences", {}).get("top_literary_styles", [])}
            matching_styles = [style for style in book.literary_style if style in user_styles]
            if matching_styles:
                matching_points.append(f"literary style ({', '.join(str(s) for s in matching_styles)})")

        # Build explanation
        if matching_points:
            matches = ", ".join(matching_points)
            explanation = f"Recommended based on your preference for {matches}."
        else:
            # If no direct matches, use a more generic explanation
            explanation = "Recommended based on overall patterns in your reading preferences."

        return explanation

    async def get_recommendations(
            self,
            preferences: UserPreferences,
            num_recommendations: int = 5
    ) -> RecommendationResponse:
        """
        Get complete book recommendations with explanations.

        Args:
            preferences: The user's reading preferences
            num_recommendations: Number of recommendations to generate

        Returns:
            RecommendationResponse object with recommendations and explanations
        """
        # Generate book recommendations
        recommended_books = await self.generate_recommendations(preferences, num_recommendations)

        # Generate explanations for each recommendation
        recommendation_reasons = await self.generate_recommendation_reasons(preferences, recommended_books)

        # Create and return the response
        return RecommendationResponse(
            input_books=preferences.liked_books,
            recommended_books=recommended_books,
            recommendation_reasons=recommendation_reasons
        )