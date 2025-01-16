from classes.discogs_genres import DiscogsGenreClassifier
from maps.discogs_to_song_styles import discogs_to_song_styles

def discogs_spotify_song_styles(audio_file):
    """
    Detects genres for the given audio file using the Discogs classifier 
    and maps them to song styles.

    Parameters:
        audio_file (str): Path to the audio file to classify.
        model_dir (str): Path to the directory containing the models and metadata.

    Returns:
        list: A sorted list of up to three song styles based on the detected genres.
    """
    
    # Initialize the Discogs genre classifier
    classifier = DiscogsGenreClassifier()

    # Classify the genres using the Discogs model
    main_genre, primary_genre, secondary_genre = classifier.classify_genres(audio_file)

    # Map the detected genres to song styles
    mapped_main_style = discogs_to_song_styles.get(main_genre, "Unknown")
    mapped_primary_style = discogs_to_song_styles.get(primary_genre, "Unknown")
    mapped_secondary_style = discogs_to_song_styles.get(secondary_genre, "Unknown")

    # Prioritize styles and remove "Unknown" and duplicates
    styles = [mapped_main_style, mapped_primary_style, mapped_secondary_style]
    styles = [style for style in styles if style != "Unknown"]
    styles = sorted(list(dict.fromkeys(styles)))  # Removes duplicates and sorts alphabetically

    # Return up to three song styles
    return styles[:2] if styles else ["None of these"]

if __name__ == "__main__":
    audio_file = "files/audio.wav"  # Replace with your audio file path

    try:
        # Call the `discogs_spotify_song_styles` function to get mapped styles
        styles = discogs_spotify_song_styles(audio_file)
        
        print("Mapped Song Styles:")
        if styles:
            for i, style in enumerate(styles, 1):
                print(f"Style {i}: {style}")
        else:
            print("No valid song styles detected.")
    except Exception as e:
        print(f"Error: {e}")
