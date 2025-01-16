import os
from classes.timbre import TimbreClassifier
def timbre(file):
    classifier = TimbreClassifier()

    try:
        # Classify approachability
        timbre = classifier.classify_timbre(file)
        return timbre
    except Exception as e:
        raise RuntimeError(f"Error finding timbre classification: {e}")
    
# Example usage
if __name__ == "__main__":
    audio_file = "files/audio.wav"
    try:
        timbre = timbre(audio_file)
        print("Timbre Scores:")
        for label, score in timbre.items():
            print(f"  {label}: {score:.4f}")
    except Exception as e:
        print(e)