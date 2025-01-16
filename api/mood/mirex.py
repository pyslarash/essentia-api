from classes.moods_mirex import MoodsMirexClassifier

def mirex(file):
    classifier = MoodsMirexClassifier()

    try:
        # Classify approachability
        mirex  = classifier.classify_moods(file)
        return mirex 
    except Exception as e:
        raise RuntimeError(f"Error finding MIREX classification: {e}")
    
# Example usage
if __name__ == "__main__":
    audio_file = "files/audio.wav"
    try:
        mirex  = mirex(audio_file)
        print("MIREX  Scores:")
        for label, score in mirex .items():
            print(f"  {label}: {score:.4f}")
    except Exception as e:
        print(e)