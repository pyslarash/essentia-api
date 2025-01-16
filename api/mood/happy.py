from classes.mood_happy import MoodHappyClassifier

def happy(file):
    classifier = MoodHappyClassifier()

    try:
        # Classify approachability
        happy = classifier.classify_mood(file)
        return happy
    except Exception as e:
        raise RuntimeError(f"Error finding happy classification: {e}")
    
# Example usage
if __name__ == "__main__":
    audio_file = "files/audio.wav"
    try:
        happy = happy(audio_file)
        print("Happy Scores:")
        for label, score in happy.items():
            print(f"  {label}: {score:.4f}")
    except Exception as e:
        print(e)