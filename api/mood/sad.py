from classes.mood_sad import MoodSadClassifier

def sad(file):
    classifier = MoodSadClassifier()

    try:
        # Classify approachability
        sad  = classifier.classify_mood(file)
        return sad 
    except Exception as e:
        raise RuntimeError(f"Error finding sad classification: {e}")
    
# Example usage
if __name__ == "__main__":
    audio_file = "files/audio.wav"
    try:
        sad  = sad(audio_file)
        print("Sad  Scores:")
        for label, score in sad .items():
            print(f"  {label}: {score:.4f}")
    except Exception as e:
        print(e)