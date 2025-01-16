from classes.discogs_genres import DiscogsGenreClassifier
from maps.discogs_to_music_cultures import discogs_to_music_cultures

def discogs_spotify_music_cultures(audio_file):
    """
    Detects genres for the given audio file using the Discogs classifier 
    and maps them to music cultures.

    Parameters:
        audio_file (str): Path to the audio file to classify.
        model_dir (str): Path to the directory containing the models and metadata.

    Returns:
        list: A sorted list of up to three music cultures based on the detected genres.
    """
    
    # Initialize the Discogs genre classifier
    classifier = DiscogsGenreClassifier()

    # Classify the genres using the Discogs model
    main_genre, primary_genre, secondary_genre = classifier.classify_genres(audio_file)

    # Map the detected genres to music cultures
    mapped_main_culture = discogs_to_music_cultures.get(main_genre, "Unknown")
    mapped_primary_culture = discogs_to_music_cultures.get(primary_genre, "Unknown")
    mapped_secondary_culture = discogs_to_music_cultures.get(secondary_genre, "Unknown")

    # Prioritize cultures and remove "Unknown" and duplicates
    cultures = [mapped_main_culture, mapped_primary_culture, mapped_secondary_culture]
    cultures = [culture for culture in cultures if culture != "Unknown"]
    cultures = sorted(list(dict.fromkeys(cultures)))  # Removes duplicates and sorts alphabetically

    # Return up to three music cultures
    return cultures[:2] if cultures else ["None of these"]

if __name__ == "__main__":
    audio_file = "files/audio.wav"  # Replace with your audio file path
    model_dir = "models"           # Path to the directory containing models and metadata

    try:
        # Call the `discogs_spotify_music_cultures` function to get mapped cultures
        cultures = discogs_spotify_music_cultures(audio_file, model_dir)
        
        print("Mapped Music Cultures:")
        if cultures:
            for i, culture in enumerate(cultures, 1):
                print(f"Culture {i}: {culture}")
        else:
            print("No valid music cultures detected.")
    except Exception as e:
        print(f"Error: {e}")
