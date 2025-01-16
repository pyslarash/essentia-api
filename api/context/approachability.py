import os
from classes.approachability import ApproachabilityClassifier

def approachability(file):
    classifier = ApproachabilityClassifier()

    try:
        # Classify approachability
        approachability_scores = classifier.classify_approachability(file)
        return approachability_scores
    except Exception as e:
        raise RuntimeError(f"Error during approachability classification: {e}")

# Example usage
if __name__ == "__main__":
    audio_file = "files/audio.wav"
    try:
        scores = approachability(audio_file)
        print("Approachability Scores:")
        for label, score in scores.items():
            print(f"  {label}: {score:.4f}")
    except Exception as e:
        print(e)