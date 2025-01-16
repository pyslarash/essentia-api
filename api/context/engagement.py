import os
from classes.engagement import EngagementClassifier

def engagement(file):
    classifier = EngagementClassifier()

    try:
        # Classify engagement
        engagement = classifier.classify_engagement(file)
        return engagement
    except Exception as e:
        raise RuntimeError(f"Error during engagement classification: {e}")

# Example usage
if __name__ == "__main__":
    audio_file = "files/audio.wav"
    try:
        engagement = engagement(audio_file)
        print("Engagement Scores:")
        for label, score in engagement.items():
            print(f"  {label}: {score:.4f}")
    except Exception as e:
        print(e)