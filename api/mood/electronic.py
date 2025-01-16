from classes.mood_electronic import MoodElectronicClassifier

def electronic(file):
    classifier = MoodElectronicClassifier()

    try:
        # Classify approachability
        electronic = classifier.classify_mood(file)
        return electronic
    except Exception as e:
        raise RuntimeError(f"Error finding electronic classification: {e}")
    
# Example usage
if __name__ == "__main__":
    audio_file = "files/audio.wav"
    try:
        electronic = electronic(audio_file)
        print("Electronic Scores:")
        for label, score in electronic.items():
            print(f"  {label}: {score:.4f}")
    except Exception as e:
        print(e)