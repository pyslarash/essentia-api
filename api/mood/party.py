from classes.mood_party import MoodPartyClassifier

def party(file):
    classifier = MoodPartyClassifier()

    try:
        # Classify approachability
        party = classifier.classify_mood(file)
        return party
    except Exception as e:
        raise RuntimeError(f"Error finding party classification: {e}")
    
# Example usage
if __name__ == "__main__":
    audio_file = "files/audio.wav"
    try:
        party = party(audio_file)
        print("Party Scores:")
        for label, score in party.items():
            print(f"  {label}: {score:.4f}")
    except Exception as e:
        print(e)