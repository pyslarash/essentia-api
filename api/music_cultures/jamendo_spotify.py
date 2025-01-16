from classes.jamendo_genres import JamendoGenreClassifier
from maps.jamendo_to_music_cultures import jamendo_to_music_cultures

def jamendo_spotify_music_cultures(audio_file):
    """
    Detects genres for the given audio file using the Jamendo classifier 
    and maps them to music cultures.

    Parameters:
        audio_file (str): Path to the audio file to classify.
        model_dir (str): Path to the directory containing the models and metadata.

    Returns:
        list: A sorted list of up to two music cultures based on the detected genres, 
              or ["None of these"] if no valid genres are selected.
    """
    # Initialize the Jamendo genre classifier
    classifier = JamendoGenreClassifier()

    try:
        # Classify the genres using the Jamendo model
        primary_genre, secondary_genre, tertiary_genre = classifier.classify_genres(audio_file)

        # Map the detected genres to music cultures
        mapped_primary = jamendo_to_music_cultures.get(primary_genre, "Unknown")
        mapped_secondary = jamendo_to_music_cultures.get(secondary_genre, "Unknown")
        mapped_tertiary = jamendo_to_music_cultures.get(tertiary_genre, "Unknown")

        # Prioritize cultures and remove "Unknown" and duplicates
        cultures = [mapped_primary, mapped_secondary, mapped_tertiary]
        cultures = [culture for culture in cultures if culture != "Unknown"]
        cultures = sorted(list(dict.fromkeys(cultures)))  # Removes duplicates and sorts alphabetically

        # Return up to two music cultures or ["None of these"] if no valid genres
        return cultures[:2] if cultures else ["None of these"]
    except Exception as e:
        raise RuntimeError(f"Error in Jamendo to music culture mapping: {e}")

if __name__ == "__main__":
    audio_file = "files/audio.wav"  # Replace with your audio file path
    model_dir = "models"           # Path to the directory containing models and metadata

    try:
        # Call the `jamendo_spotify_music_cultures` function to get mapped cultures
        cultures = jamendo_spotify_music_cultures(audio_file, model_dir)
        
        print("Mapped Music Cultures (Alphabetical Order):")
        if cultures:
            for i, culture in enumerate(cultures, 1):
                print(f"Culture {i}: {culture}")
        else:
            print("No valid music cultures detected.")
    except Exception as e:
        print(f"Error: {e}")
