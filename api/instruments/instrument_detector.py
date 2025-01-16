from classes.jamendo_instruments import JamendoInstrumentClassifier

def instrument_detector(file):
    """
    Detects instruments in an audio file using JamendoInstrumentClassifier.

    Args:
        file (str): Path to the audio file.

    Returns:
        list: A list of detected instruments sorted alphabetically.
    """
    classifier = JamendoInstrumentClassifier()

    try:
        # Classify instruments
        detected_instruments = classifier.classify_instruments(file)

        # Return detected instruments sorted alphabetically
        return sorted(detected_instruments)
    except Exception as e:
        raise RuntimeError(f"Error during instrument classification: {e}")

# Example usage
if __name__ == "__main__":
    audio_file = "files/audio.wav"
    try:
        detected_instruments = instrument_detector(audio_file)
        print("Detected Instruments:")
        print(", ".join(detected_instruments))
    except Exception as e:
        print(e)
