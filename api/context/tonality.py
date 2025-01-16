import os
from classes.tonality import TonalityClassifier

def tonality(file):
    classifier = TonalityClassifier()

    try:
        # Classify tonality
        tonality = classifier.classify_tonality(file)
        return tonality
    except Exception as e:
        raise RuntimeError(f"Error during engagement classification: {e}")

# Example usage
if __name__ == "__main__":
    audio_file = "files/audio.wav"
    try:
        tonality = tonality(audio_file)
        print("Tonality Scores:")
        for label, score in tonality.items():
            print(f"  {label}: {score:.4f}")
    except Exception as e:
        print(e)