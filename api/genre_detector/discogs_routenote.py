from classes.discogs_genres import DiscogsGenreClassifier
from maps.discogs_to_routenote import discogs_to_routenote
from dotenv import load_dotenv

load_dotenv()

def discogs_routenote(audio_file):
    """
    Detects genres for the given audio file using the Discogs classifier and maps them to RouteNote genres.

    Parameters:
        audio_file (str): Path to the audio file to classify.
        model_dir (str): Path to the directory containing the models and metadata.

    Returns:
        list: A sorted list of mapped genres in alphabetical order.
    """
    
    # Initialize the Discogs genre classifier
    classifier = DiscogsGenreClassifier()

    # Classify the genres using the Discogs model
    main_genre, primary_genre, secondary_genre = classifier.classify_genres(audio_file)

    # Map the detected genres to RouteNote categories
    mapped_main_genre = discogs_to_routenote.get(main_genre, "Unknown")
    mapped_primary_genre = discogs_to_routenote.get(primary_genre, "Unknown")
    mapped_secondary_genre = discogs_to_routenote.get(secondary_genre, "Unknown")

    # Prioritize genres and remove "Unknown" and duplicates
    genres = [mapped_main_genre, mapped_primary_genre, mapped_secondary_genre]
    genres = [genre for genre in genres if genre != "Unknown"]
    genres = list(dict.fromkeys(genres))  # Removes duplicates while preserving order

    # Return sorted genres in alphabetical order
    return sorted(genres)

if __name__ == "__main__":
    audio_file = "files/audio.wav"  # Replace with your audio file path

    try:
        # Call the `discogs_routenote` function to get mapped genres
        genres = discogs_routenote(audio_file)
        
        print("Mapped Genres:")
        if genres:
            for i, genre in enumerate(genres, 1):
                print(f"Genre {i}: {genre}")
        else:
            print("No valid genres detected.")
    except Exception as e:
        print(f"Error: {e}")
