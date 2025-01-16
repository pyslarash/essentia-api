from classes.mood_relaxed import MoodRelaxedClassifier

def relaxed(file):
    classifier = MoodRelaxedClassifier()

    try:
        # Classify approachability
        relaxed  = classifier.classify_mood(file)
        return relaxed 
    except Exception as e:
        raise RuntimeError(f"Error finding relaxed classification: {e}")
    
# Example usage
if __name__ == "__main__":
    audio_file = "files/audio.wav"
    try:
        relaxed  = relaxed(audio_file)
        print("Relaxed  Scores:")
        for label, score in relaxed .items():
            print(f"  {label}: {score:.4f}")
    except Exception as e:
        print(e)