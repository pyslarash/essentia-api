from classes.jamendo_genres import JamendoGenreClassifier
from maps.jamendo_to_routenote import jamendo_to_routenote

def jamendo_routenote(audio_file):
    """
    Detects genres for the given audio file using the Jamendo classifier and maps them to RouteNote genres.

    Parameters:
        audio_file (str): Path to the audio file to classify.
        model_dir (str): Path to the directory containing the models and metadata.

    Returns:
        list: A sorted list of up to two mapped genres in alphabetical order.
    """
    # Initialize the Jamendo genre classifier
    classifier = JamendoGenreClassifier()

    try:
        # Classify the genres using the Jamendo model
        primary_genre, secondary_genre, tertiary_genre = classifier.classify_genres(audio_file)

        # Map the detected genres to RouteNote categories
        mapped_primary = jamendo_to_routenote.get(primary_genre, "Unknown")
        mapped_secondary = jamendo_to_routenote.get(secondary_genre, "Unknown")
        mapped_tertiary = jamendo_to_routenote.get(tertiary_genre, "Unknown")

        # Prioritize genres and remove "Unknown" and duplicates
        genres = [mapped_primary, mapped_secondary, mapped_tertiary]
        genres = [genre for genre in genres if genre != "Unknown"]
        genres = list(dict.fromkeys(genres))  # Removes duplicates while preserving order

        # Return up to two genres in alphabetical order
        return sorted(genres)[:2]
    except Exception as e:
        raise RuntimeError(f"Error in Jamendo to RouteNote genre mapping: {e}")

if __name__ == "__main__":
    audio_file = "files/audio.wav"  # Replace with your audio file path

    try:
        # Call the `jamendo_routenote` function to get mapped genres
        genres = jamendo_routenote(audio_file)
        
        print("Mapped Genres (Alphabetical Order):")
        if genres:
            for i, genre in enumerate(genres, 1):
                print(f"Genre {i}: {genre}")
        else:
            print("No valid genres detected.")
    except Exception as e:
        print(f"Error: {e}")
