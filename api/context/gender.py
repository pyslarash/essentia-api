import os
from classes.voice_gender import VoiceGenderClassifier

def gender(file):
    classifier = VoiceGenderClassifier()

    try:
        # Classify approachability
        gender = classifier.classify_gender(file)
        return gender
    except Exception as e:
        raise RuntimeError(f"Error finding voice gender classification: {e}")
    
# Example usage
if __name__ == "__main__":
    audio_file = "files/audio.wav"
    try:
        gender = gender(audio_file)
        print("Gender Scores:")
        for label, score in gender.items():
            print(f"  {label}: {score:.4f}")
    except Exception as e:
        print(e)