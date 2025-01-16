import os
from essentia.standard import (
    MonoLoader,
    FrameCutter,
    Windowing,
    Spectrum,
    SpectralPeaks,
    HPCP,
    KeyExtractor,
    RhythmExtractor2013,
    ChordsDetection,
    DynamicComplexity,
    FrameGenerator
)

class TrackAnalysis:
    """
    Extracts basic music features such as key, tempo, chords, and other fundamental descriptors.
    """

    def __init__(self):
        """
        Initializes the feature extractor algorithms.
        """
        self.frame_cutter = FrameCutter(frameSize=4096, hopSize=2048)
        self.windowing = Windowing(type='blackmanharris62')
        self.spectrum = Spectrum()
        self.spectral_peaks = SpectralPeaks()
        self.hpcp = HPCP()
        self.key_extractor = KeyExtractor()
        self.rhythm_extractor = RhythmExtractor2013()
        self.chords_detection = ChordsDetection()
        self.dynamic_complexity_extractor = DynamicComplexity()

    def load_audio(self, audio_file, sample_rate=44100):
        """
        Loads the audio file and resamples it to the desired sample rate.
        """
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"Audio file not found: {audio_file}")
        loader = MonoLoader(filename=audio_file, sampleRate=sample_rate)
        return loader()

    def compute_hpcp(self, audio):
        """
        Computes the HPCP (Harmonic Pitch Class Profile) from the audio signal.
        """
        hpcp_frames = []
        for frame in FrameGenerator(audio, frameSize=4096, hopSize=2048, startFromZero=True):
            windowed_frame = self.windowing(frame)
            spectrum = self.spectrum(windowed_frame)
            frequencies, magnitudes = self.spectral_peaks(spectrum)
            hpcp = self.hpcp(frequencies, magnitudes)
            hpcp_frames.append(hpcp)
        return hpcp_frames

    def extract_features(self, audio_file):
        """
        Extracts key, tempo, chords, and other basic features from the audio file.

        Returns:
            dict: A dictionary containing extracted features.
        """
        # Load audio
        audio = self.load_audio(audio_file)

        # Extract key and scale
        key, scale, key_strength = self.key_extractor(audio)

        # Extract rhythm (tempo and beats)
        bpm, beats, beats_confidence, _, _ = self.rhythm_extractor(audio)

        # Compute HPCP frames
        hpcp_frames = self.compute_hpcp(audio)

        # Detect chords
        chords, chords_strength = self.chords_detection(hpcp_frames)
        chords_with_timestamps = [[chord, float(round(beats[i], 2))] for i, chord in enumerate(chords) if i < len(beats)]

        # Extract dynamic complexity
        dynamic_complexity = self.dynamic_complexity_extractor(audio)

        # Compile results, ensuring all numerical values are Python native types
        features = {
            "key": key,
            "scale": scale,
            "key_strength": f"{float(key_strength) * 100:.0f}%",
            "bpm": float(bpm),
            "number_of_beats": len(beats),
            "beat_confidence": f"{float(beats_confidence) / 5.32 * 100:.0f}%",
            "chords": chords_with_timestamps,
            "dynamic_complexity": f"{float(dynamic_complexity[0]):.2f}",
            "loudness": f"{float(dynamic_complexity[1]):.2f} dB",
        }

        return features

    @staticmethod
    def format_features(features):
        output = [f"Extracted Music Features:"]
        output.append(f"  Key: {features['key']}")
        output.append(f"  Scale: {features['scale']}")
        output.append(f"  Key Strength: {features['key_strength']}")
        output.append(f"  BPM: {features['bpm']:.2f}") 
        output.append(f"  Number of Beats: {features['number_of_beats']}")
        output.append(f"  Beat Confidence: {features['beat_confidence']}")
        output.append("  Chords:")
        for chord, timestamp in features["chords"]:
            output.append(f"    - [{chord}, {timestamp:.2f}s]")
        output.append(f"  Dynamic Complexity: {features['dynamic_complexity']}")
        output.append(f"  Loudness: {features['loudness']}")
        return "\n".join(output)


def main():
    audio_file = "files/audio.wav"
    extractor = TrackAnalysis()

    try:
        # Extract features
        features = extractor.extract_features(audio_file)

        # Format features for readability
        readable_output = extractor.format_features(features)
        print(readable_output)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
