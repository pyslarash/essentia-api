from classes.jamendo_genres import JamendoGenreClassifier

def jamendo(file):
    """
    Function to classify the genres of an audio file using the JamendoGenreClassifier class.

    Args:
        file (str): Path to the audio file.

    Returns:
        list: A list of genres (primary, secondary, and tertiary) sorted alphabetically.
    """

    # Initialize the classifier
    classifier = JamendoGenreClassifier()

    try:
        # Classify the genres of the provided audio file
        primary_genre, secondary_genre, tertiary_genre = classifier.classify_genres(file)

        # Remove duplicates and sort genres alphabetically
        genres = [primary_genre, secondary_genre, tertiary_genre]
        genres = [genre for genre in genres if genre]  # Remove None values
        genres = list(dict.fromkeys(genres))  # Remove duplicates while preserving order
        return sorted(genres)  # Return genres in alphabetical order
    except Exception as e:
        raise RuntimeError(f"Error in genre classification: {e}")

# Example usage
if __name__ == "__main__":
    audio_file = "files/audio.wav"
    try:
        genres = jamendo(audio_file)
        print("Detected Genres (Alphabetical Order):")
        for genre in genres:
            print(genre)
    except Exception as e:
        print(f"Error: {e}")
