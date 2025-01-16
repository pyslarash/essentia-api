import os
from classes.yamnet_audio_event import YamNetAudioEventClassifier

def audio_events(file):
    """
    Classifies audio events using the YamNetAudioEventClassifier.

    Args:
        file (str): Path to the audio file.

    Returns:
        list: The top 10 audio events detected.
    """
    classifier = YamNetAudioEventClassifier()

    try:
        # Classify audio events
        detected_events = classifier.classify_audio_events(file)
        return detected_events
    except Exception as e:
        raise RuntimeError(f"Error during audio events classification: {e}")

# Example usage
if __name__ == "__main__":
    audio_file = "files/audio.wav"
    try:
        detected_events = audio_events(audio_file)
        print("Detected Audio Events:")
        print(", ".join(detected_events))
    except Exception as e:
        print(e)
