from classes.jamendo_genres import JamendoGenreClassifier
from maps.jamendo_to_spotify import jamendo_to_spotify

def jamendo_spotify(audio_file):
    """
    Detects genres for the given audio file using the Jamendo classifier and maps them to Spotify genres.

    Parameters:
        audio_file (str): Path to the audio file to classify.
        model_dir (str): Path to the directory containing the models and metadata.

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

if __name__ == "__main__":
    audio_file = "files/audio.wav"  # Replace with your audio file path

    try:
        # Call the `jamendo_spotify` function to get mapped genres
        genres = jamendo_spotify(audio_file)
        
        print("Mapped Spotify Genres (Alphabetical Order):")
        if genres:
            for i, genre in enumerate(genres, 1):
                print(f"Genre {i}: {genre}")
        else:
            print("No valid genres detected.")
    except Exception as e:
        print(f"Error: {e}")
