from classes.discogs_genres import DiscogsGenreClassifier

def discogs(file):
    """
    Function to classify the genres of an audio file using the DiscogsGenreClassifier class.

    Args:
        file (str): Path to the audio file.

    Returns:
        dict: A dictionary containing main_genre, primary_genre, and secondary_genre.
    """

    # Initialize the classifier
    classifier = DiscogsGenreClassifier()

    try:
        # Classify the genres of the provided audio file
        main_genre, primary_genre, secondary_genre = classifier.classify_genres(file)

        # Return the genres as a dictionary
        return {
            "main_genre": main_genre,
            "primary_genre": primary_genre,
            "secondary_genre": secondary_genre
        }
    except Exception as e:
        raise RuntimeError(f"Error in genre classification: {e}")

# Example usage
if __name__ == "__main__":
    audio_file = "files/audio.wav"
    try:
        genres = discogs(audio_file)
        print("Detected Genres (Alphabetical Order):")
        for genre in genres:
            print(genre)
    except Exception as e:
        print(f"Error: {e}")
