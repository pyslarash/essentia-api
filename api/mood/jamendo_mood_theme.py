from classes.jamendo_mood_and_theme import JamendoMoodAndThemeClassifier

def jamendo_mood_theme(file, top_n=3):
    """
    Classifies the mood and theme of an audio file using the JamendoMoodAndThemeClassifier.

    Args:
        file (str): Path to the audio file.
        top_n (int): Number of top moods/themes to return.

    Returns:
        list: A sorted list of the top moods/themes detected.
    """
    classifier = JamendoMoodAndThemeClassifier()

    try:
        # Classify mood and theme
        moods_and_themes = classifier.classify_mood_and_theme(file, top_n=top_n)
        
        # Return sorted moods and themes
        return sorted(moods_and_themes)
    except Exception as e:
        raise RuntimeError(f"Error classifying mood and theme: {e}")

# Example usage
if __name__ == "__main__":
    audio_file = "files/audio.wav"
    try:
        top_moods_and_themes = jamendo_mood_theme(audio_file, top_n=3)
        print("Top 3 Moods and Themes (Alphabetical Order):")
        print(top_moods_and_themes)
    except Exception as e:
        print(e)
