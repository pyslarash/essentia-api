from classes.danceability import DanceabilityClassifier

def danceability(file):
    classifier = DanceabilityClassifier()

    try:
        # Classify approachability
        dancebility = classifier.classify_danceability(file)
        return dancebility
    except Exception as e:
        raise RuntimeError(f"Error during dancebility classification: {e}")
    
# Example usage
if __name__ == "__main__":
    audio_file = "files/audio.wav"
    try:
        arouseness = danceability(audio_file)
        print("Dancebility Scores:")
        for label, score in arouseness.items():
            print(f"  {label}: {score:.4f}")
    except Exception as e:
        print(e)