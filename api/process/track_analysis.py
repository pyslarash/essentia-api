import os
from classes.track_analysis import TrackAnalysis

def track_analysis(file):
    """
    Analyzes music features such as key, tempo, chords, and more using TrackAnalysis.

    Args:
        file (str): Path to the audio file.

    Returns:
        dict: A dictionary with the extracted music features.
    """
    extractor = TrackAnalysis()

    try:
        # Extract features
        features = extractor.extract_features(file)
        return features
    except Exception as e:
        raise RuntimeError(f"Error during track analysis: {e}")

# Example usage
if __name__ == "__main__":
    audio_file = "files/audio.wav"
    try:
        readable_output = track_analysis(audio_file)
        print(readable_output)
    except Exception as e:
        print(e)
