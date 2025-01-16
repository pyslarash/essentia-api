from classes.jamendo_instruments import JamendoInstrumentClassifier
from maps.jamendo_to_instruments import jamendo_to_instruments

def instrument_detector_spotify(file):
    """
    Detects instruments in an audio file using JamendoInstrumentClassifier and maps them to Spotify-compatible categories.

    Args:
        file (str): Path to the audio file.

    Returns:
        list: A list of detected instruments mapped to Spotify-compatible categories, sorted alphabetically, without duplicates.
    """
    classifier = JamendoInstrumentClassifier()

    try:
        # Classify instruments
        detected_instruments = classifier.classify_instruments(file)

        # Map instruments to Spotify-compatible categories
        mapped_instruments = {
            jamendo_to_instruments[instrument.lower()]
            for instrument in detected_instruments
            if instrument.lower() in jamendo_to_instruments
        }

        # Return unique mapped instruments sorted alphabetically
        return sorted(mapped_instruments)
    except Exception as e:
        raise RuntimeError(f"Error during instrument classification: {e}")

# Example usage
if __name__ == "__main__":
    audio_file = "files/audio.wav"
    try:
        spotify_instruments = instrument_detector_spotify(audio_file)
        print("Mapped Instruments (Spotify Compatible):")
        print(", ".join(spotify_instruments))
    except Exception as e:
        print(e)
