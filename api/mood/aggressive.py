from classes.mood_aggressive import MoodAggressiveClassifier

def aggressive(file):
    classifier = MoodAggressiveClassifier()

    try:
        # Classify approachability
        aggressive = classifier.classify_mood(file)
        return aggressive
    except Exception as e:
        raise RuntimeError(f"Error finding aggressive classification: {e}")
    
# Example usage
if __name__ == "__main__":
    audio_file = "files/audio.wav"
    try:
        aggressive = aggressive(audio_file)
        print("Aggressive Scores:")
        for label, score in aggressive.items():
            print(f"  {label}: {score:.4f}")
    except Exception as e:
        print(e)