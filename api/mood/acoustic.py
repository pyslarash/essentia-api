from classes.mood_acoustic import MoodAcousticClassifier

def acoustic(file):
    classifier = MoodAcousticClassifier()

    try:
        # Classify approachability
        acoustic = classifier.classify_mood(file)
        return acoustic
    except Exception as e:
        raise RuntimeError(f"Error finding acoustic classification: {e}")
    
# Example usage
if __name__ == "__main__":
    audio_file = "files/audio.wav"
    try:
        acoustic = acoustic(audio_file)
        print("Acoustic Scores:")
        for label, score in acoustic.items():
            print(f"  {label}: {score:.4f}")
    except Exception as e:
        print(e)