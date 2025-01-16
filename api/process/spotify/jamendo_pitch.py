from classes.jamendo_genres import JamendoGenreClassifier
from classes.jamendo_instruments import JamendoInstrumentClassifier
from classes.jamendo_mood_and_theme import JamendoMoodAndThemeClassifier
from maps.jamendo_to_spotify import jamendo_to_spotify
from maps.jamendo_to_music_cultures import jamendo_to_music_cultures
from maps.jamendo_to_song_styles import jamendo_to_song_styles
from maps.jamendo_to_instruments import jamendo_to_instruments
from maps.jamendo_to_moods import jamendo_to_moods

def apply_fallback_and_deduplicate(category_items, fallback="None of these"):
    """
    Ensures a category list has fallback if empty and removes duplicates.

    Args:
        category_items (list): The list of items for the category.
        fallback (str): The fallback value to return if the list is empty.

    Returns:
        list: A deduplicated list or the fallback value as a list if empty.
    """
    category_items = list(dict.fromkeys(category_items))  # Remove duplicates while preserving order
    return category_items if category_items else [fallback]

def detect_genres(audio_file):
    """
    Detects genres for the given audio file using the Jamendo classifier and maps them to Spotify genres.

    Parameters:
        audio_file (str): Path to the audio file to classify.

    Returns:
        list: A sorted list of up to three mapped genres in alphabetical order, 
              or ["None of these"] if no valid genres are selected.
    """
    # Initialize the Jamendo genre classifier
    classifier = JamendoGenreClassifier()

    try:
        # Classify the genres using the Jamendo model
        primary_genre, secondary_genre, tertiary_genre = classifier.classify_genres(audio_file)

        # Map the detected genres to Spotify categories
        mapped_primary = jamendo_to_spotify.get(primary_genre, "None of these")
        mapped_secondary = jamendo_to_spotify.get(secondary_genre, "None of these")
        mapped_tertiary = jamendo_to_spotify.get(tertiary_genre, "None of these")

        # Prioritize genres and remove "None of these" and duplicates
        genres = [mapped_primary, mapped_secondary, mapped_tertiary]
        genres = [genre for genre in genres if genre != "None of these"]
        genres = list(dict.fromkeys(genres))  # Removes duplicates while preserving order

        # Return up to three genres in alphabetical order, or "None of these" if no valid genres
        return sorted(genres)[:3] if genres else ["None of these"]
    except Exception as e:
        raise RuntimeError(f"Error in Jamendo to Spotify genre mapping: {e}")

def jamendo_spotify_pitch(file):
    """
    Combines genre, music culture, song style, instrument, and mood mapping for Spotify pitch using Jamendo classifiers.

    Args:
        file (str): Path to the audio file.

    Returns:
        dict: A dictionary with Spotify genres, music cultures, song styles, instruments, and moods.
    """
    # Initialize classifiers
    instrument_classifier = JamendoInstrumentClassifier()
    mood_classifier = JamendoMoodAndThemeClassifier()

    try:
        # Step 1: Detect and map genres (aligned with the second implementation)
        spotify_genres = detect_genres(file)

        # Map genres to music cultures
        genre_classifier = JamendoGenreClassifier()
        primary_genre, secondary_genre, tertiary_genre = genre_classifier.classify_genres(file)

        mapped_cultures = [
            jamendo_to_music_cultures.get(primary_genre),
            jamendo_to_music_cultures.get(secondary_genre),
            jamendo_to_music_cultures.get(tertiary_genre),
        ]
        spotify_cultures = apply_fallback_and_deduplicate(
            [culture for culture in mapped_cultures if culture][:2]
        )

        # Map genres to song styles
        mapped_styles = [
            jamendo_to_song_styles.get(primary_genre),
            jamendo_to_song_styles.get(secondary_genre),
            jamendo_to_song_styles.get(tertiary_genre),
        ]
        spotify_styles = apply_fallback_and_deduplicate(
            [style for style in mapped_styles if style][:2]
        )

        # Step 2: Classify instruments using Jamendo classifier
        detected_instruments = instrument_classifier.classify_instruments(file)

        # Map instruments to Spotify-compatible categories
        spotify_instruments = sorted({
            jamendo_to_instruments[instrument.lower()]
            for instrument in detected_instruments
            if instrument.lower() in jamendo_to_instruments
        })
        spotify_instruments = apply_fallback_and_deduplicate(spotify_instruments)

        # Step 3: Classify moods and themes using Jamendo classifier
        moods_and_themes = mood_classifier.classify_mood_and_theme(file, top_n=2)

        # Map the detected moods and themes to Spotify-compatible moods
        spotify_moods = sorted({
            jamendo_to_moods[mood.lower()]
            for mood in moods_and_themes
            if mood.lower() in jamendo_to_moods
        })
        spotify_moods = apply_fallback_and_deduplicate(spotify_moods)

        # Combine results into a dictionary
        result = {
            "Spotify Genres": spotify_genres,
            "Spotify Music Cultures": spotify_cultures,
            "Spotify Song Styles": spotify_styles,
            "Spotify Instruments": spotify_instruments,
            "Spotify Moods": spotify_moods,
        }

        return result
    except Exception as e:
        raise RuntimeError(f"Error during Spotify pitch preparation: {e}")

# Example usage
if __name__ == "__main__":
    audio_file = "files/audio.wav"  # Replace with your audio file path
    try:
        spotify_pitch = jamendo_spotify_pitch(audio_file)

        print("Spotify Pitch Results:")
        for category, items in spotify_pitch.items():
            print(f"{category}: {', '.join(items)}")
    except Exception as e:
        print(f"Error: {e}")
