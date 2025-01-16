from classes.jamendo_genres import JamendoGenreClassifier
from maps.jamendo_to_song_styles import jamendo_to_song_styles

def jamendo_spotify_song_styles(audio_file):
    """
    Detects genres for the given audio file using the Jamendo classifier 
    and maps them to song styles.

    Parameters:
        audio_file (str): Path to the audio file to classify.
        model_dir (str): Path to the directory containing the models and metadata.

    Returns:
        list: A sorted list of up to two song styles based on the detected genres.
    """
    # Initialize the Jamendo genre classifier
    classifier = JamendoGenreClassifier()

    try:
        # Classify the genres using the Jamendo model
        primary_genre, secondary_genre, tertiary_genre = classifier.classify_genres(audio_file)

        # Map the detected genres to song styles
        mapped_primary_style = jamendo_to_song_styles.get(primary_genre, "Unknown")
        mapped_secondary_style = jamendo_to_song_styles.get(secondary_genre, "Unknown")
        mapped_tertiary_style = jamendo_to_song_styles.get(tertiary_genre, "Unknown")

        # Prioritize styles and remove "Unknown" and duplicates
        styles = [mapped_primary_style, mapped_secondary_style, mapped_tertiary_style]
        styles = [style for style in styles if style != "Unknown"]
        styles = sorted(list(dict.fromkeys(styles)))  # Removes duplicates and sorts alphabetically

        # Return up to two song styles or ["None of these"] if no valid styles
        return styles[:2] if styles else ["None of these"]
    except Exception as e:
        raise RuntimeError(f"Error in Jamendo to song style mapping: {e}")

if __name__ == "__main__":
    audio_file = "files/audio.wav"  # Replace with your audio file path

    try:
        # Call the `jamendo_spotify_song_styles` function to get mapped styles
        styles = jamendo_spotify_song_styles(audio_file)
        
        print("Mapped Song Styles (Alphabetical Order):")
        if styles:
            for i, style in enumerate(styles, 1):
                print(f"Style {i}: {style}")
        else:
            print("No valid song styles detected.")
    except Exception as e:
        print(f"Error: {e}")
