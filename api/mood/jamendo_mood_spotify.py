from classes.jamendo_mood_and_theme import JamendoMoodAndThemeClassifier
from maps.jamendo_to_moods import jamendo_to_moods

def jamendo_mood_spotify(file, top_n=3):
    """
    Classifies the mood and theme of an audio file using the JamendoMoodAndThemeClassifier
    and maps them to Spotify-compatible mood categories.

    Args:
        file (str): Path to the audio file.
        top_n (int): Number of top moods/themes to return before mapping.

    Returns:
        list: A sorted list of Spotify-compatible moods without repetition. If nothing is found, returns ["None of these"].
    """
    classifier = JamendoMoodAndThemeClassifier()

    try:
        # Classify mood and theme
        moods_and_themes = classifier.classify_mood_and_theme(file, top_n=top_n)

        # Map the detected moods and themes to Spotify-compatible moods
        mapped_moods = {
            jamendo_to_moods[mood.lower()] 
            for mood in moods_and_themes 
            if mood.lower() in jamendo_to_moods
        }

        # Return sorted list of unique mapped moods or "None of these" if empty
        return sorted(mapped_moods) if mapped_moods else ["None of these"]
    except Exception as e:
        raise RuntimeError(f"Error mapping Jamendo moods to Spotify: {e}")

# Example usage
if __name__ == "__main__":
    audio_file = "files/audio.wav"
    try:
        spotify_moods = jamendo_mood_spotify(audio_file, top_n=3)
        print("Mapped Spotify Moods (Alphabetical Order):")
        print(", ".join(spotify_moods))
    except Exception as e:
        print(e)
