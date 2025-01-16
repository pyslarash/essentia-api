import os
from classes.arousal_valence_emomusic_musicnn import ArousalValenceEmomusicMusiCNNClassifier

def arouseness_em(file):
    classifier = ArousalValenceEmomusicMusiCNNClassifier()

    try:
        # Classify approachability
        arouseness_em = classifier.classify_arousal_valence(file)
        return arouseness_em
    except Exception as e:
        raise RuntimeError(f"Error during arousal and valence classification: {e}")
    
# Example usage
if __name__ == "__main__":
    audio_file = "files/audio.wav"
    try:
        arouseness = arouseness_em(audio_file)
        print("Arousal and Valence Scores:")
        for label, score in arouseness.items():
            print(f"  {label}: {score:.4f}")
    except Exception as e:
        print(e)