import os
from classes.voice_instrumental import VoiceInstrumentalClassifier

def instrumental(file):
    classifier = VoiceInstrumentalClassifier()

    try:
        # Classify approachability
        dancebility = classifier.classify_voice_instrumental(file)
        return dancebility
    except Exception as e:
        raise RuntimeError(f"Error finding voice/instrumental classification: {e}")
    
# Example usage
if __name__ == "__main__":
    audio_file = "files/audio.wav"
    try:
        instrumental = instrumental(audio_file)
        print("Instrumental and Vocal Scores:")
        for label, score in instrumental.items():
            print(f"  {label}: {score:.4f}")
    except Exception as e:
        print(e)