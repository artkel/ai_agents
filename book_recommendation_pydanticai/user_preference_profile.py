from models import UserPreferences

def analyze_genre_preferences(preferences: UserPreferences) -> dict:
    """Analyze genre distribution and relative importance."""
    genre_counts = {}
    for book in preferences.liked_books:
        for genre in book.genres:
            genre_counts[genre] = genre_counts.get(genre, 0) + 1

    # Calculate percentage distribution
    total = sum(genre_counts.values())
    if total > 0:  # Avoid division by zero
        genre_distribution = {genre: count / total for genre, count in genre_counts.items()}
    else:
        genre_distribution = {}

    return {
        "counts": genre_counts,
        "distribution": genre_distribution
    }


def analyze_author_preferences(preferences: UserPreferences) -> dict:
    """Track author preferences and their significance."""
    author_counts = {}
    for book in preferences.liked_books:
        author_counts[book.author] = author_counts.get(book.author, 0) + 1

    # Calculate significance (multiple books by same author suggests stronger preference)
    total_books = len(preferences.liked_books)
    if total_books > 0:  # Avoid division by zero
        author_significance = {author: count / total_books for author, count in author_counts.items()}
    else:
        author_significance = {}

    return {
        "counts": author_counts,
        "significance": author_significance
    }


def analyze_mood_preferences(preferences: UserPreferences) -> dict:
    """Map the emotional tone preferences of the user."""
    mood_counts = {}
    for book in preferences.liked_books:
        for mood in book.mood:
            mood_counts[mood] = mood_counts.get(mood, 0) + 1

    # Look for genre-mood correlations
    genre_mood_correlations = {}
    for book in preferences.liked_books:
        for genre in book.genres:
            for mood in book.mood:
                key = (genre, mood)
                genre_mood_correlations[key] = genre_mood_correlations.get(key, 0) + 1

    return {
        "counts": mood_counts,
        "genre_correlations": genre_mood_correlations
    }


def analyze_theme_patterns(preferences: UserPreferences) -> dict:
    """Identify recurring themes in the user's preferences."""
    theme_counts = {}
    for book in preferences.liked_books:
        for theme in book.themes:
            theme_counts[theme] = theme_counts.get(theme, 0) + 1

    # Find co-occurring themes
    theme_pairs = {}
    for book in preferences.liked_books:
        if len(book.themes) > 1:
            for i, theme1 in enumerate(book.themes):
                for theme2 in book.themes[i + 1:]:
                    pair = tuple(sorted([theme1, theme2]))
                    theme_pairs[pair] = theme_pairs.get(pair, 0) + 1

    return {
        "counts": theme_counts,
        "co_occurrences": theme_pairs
    }


def analyze_literary_style_preferences(preferences: UserPreferences) -> dict:
    """Analyze preferences for literary styles and movements."""
    style_counts = {}
    for book in preferences.liked_books:
        # Check if the book has literary_style attribute and it's not empty
        if hasattr(book, 'literary_style') and book.literary_style:
            for style in book.literary_style:
                style_counts[style] = style_counts.get(style, 0) + 1

    # Look for era-style correlations
    era_style_correlations = {}
    dated_books = [b for b in preferences.liked_books if b.year is not None
                   and hasattr(b, 'literary_style') and b.literary_style]

    for book in dated_books:
        era = get_era(book.year)  # We'll define this function below
        for style in book.literary_style:
            key = (era, style)
            era_style_correlations[key] = era_style_correlations.get(key, 0) + 1

    return {
        "counts": style_counts,
        "era_correlations": era_style_correlations
    }


def get_era(year: int) -> str:
    """Determine the literary era based on publication year."""
    if year < 1800:
        return "pre_1800"
    elif year < 1850:
        return "romantic_1800_1850"
    elif year < 1900:
        return "realist_1850_1900"
    elif year < 1945:
        return "modernist_1900_1945"
    elif year < 1970:
        return "postwar_1945_1970"
    elif year < 2000:
        return "postmodern_1970_2000"
    else:
        return "contemporary_post_2000"


def build_user_preference_profile(preferences: UserPreferences) -> dict:
    """Build a comprehensive profile of user preferences."""
    profile = {
        "genres": analyze_genre_preferences(preferences),
        "themes": analyze_theme_patterns(preferences),
        "moods": analyze_mood_preferences(preferences),
        "authors": analyze_author_preferences(preferences),
        "literary_styles": analyze_literary_style_preferences(preferences)
    }

    # Extract top preferences for easy access
    top_preferences = {
        "top_genres": sorted(profile["genres"]["counts"].items(), key=lambda x: x[1], reverse=True)[:3],
        "top_themes": sorted(profile["themes"]["counts"].items(), key=lambda x: x[1], reverse=True)[:3],
        "top_moods": sorted(profile["moods"]["counts"].items(), key=lambda x: x[1], reverse=True)[:2],
        "favorite_authors": [author for author, count in profile["authors"]["counts"].items() if count > 1],
        "top_literary_styles": sorted(profile["literary_styles"]["counts"].items(), key=lambda x: x[1], reverse=True)[:2]
    }

    profile["top_preferences"] = top_preferences
    return profile