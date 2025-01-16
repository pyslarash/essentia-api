from classes.discogs_genres import DiscogsGenreClassifier
from maps.discogs_to_spotify import discogs_to_spotify

def discogs_spotify(audio_file):
    """
    Detects genres for the given audio file using the Discogs classifier and maps them to Spotify genres.

    Parameters:
        audio_file (str): Path to the audio file to classify.

    Returns:
        list: A list of up to three genres mapped to Spotify categories, sorted alphabetically.
    """
    
    # Initialize the Discogs genre classifier
    classifier = DiscogsGenreClassifier()

    # Classify the genres using the Discogs model
    main_genre, primary_genre, secondary_genre = classifier.classify_genres(audio_file)

    # Map the detected genres to Spotify categories
    mapped_main_genre = discogs_to_spotify.get(main_genre, "Unknown")
    mapped_primary_genre = discogs_to_spotify.get(primary_genre, "Unknown")
    mapped_secondary_genre = discogs_to_spotify.get(secondary_genre, "Unknown")

    # Prioritize genres and remove "Unknown" and duplicates
    genres = [mapped_main_genre, mapped_primary_genre, mapped_secondary_genre]
    genres = [genre for genre in genres if genre != "Unknown"]
    genres = list(dict.fromkeys(genres))  # Removes duplicates while preserving order

    # Return up to three genres, sorted alphabetically
    return sorted(genres[:3])

if __name__ == "__main__":
    audio_file = "files/audio.wav"  # Replace with your audio file path

    try:
        # Call the `discogs_spotify` function to get mapped genres
        genres = discogs_spotify(audio_file)
        
        print("Mapped Spotify Genres:")
        if genres:
            for i, genre in enumerate(genres, 1):
                print(f"Genre {i}: {genre}")
        else:
            print("No valid genres detected.")
    except Exception as e:
        print(f"Error: {e}")
