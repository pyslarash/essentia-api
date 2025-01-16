import os
import json
import numpy as np
from dotenv import load_dotenv

load_dotenv()

MODELS = os.getenv('MODELS')

from essentia.standard import (
    MonoLoader,
    TensorflowPredictEffnetDiscogs,
    TensorflowPredict2D
)

class JamendoInstrumentClassifier:
    """
    1) Extract embeddings from discogs-effnet-bs64-1.pb
    2) Classify embeddings using genre_discogs400-discogs-effnet-1.pb
    """

    def __init__(self):
        """
        model_dir should contain:

        - discogs-effnet-bs64-1.pb
            (embedding model)
        - genre_discogs400-discogs-effnet-1.pb
            (classification model)
        - genre_discogs400-discogs-effnet-1.json
            (metadata, including "classes")
        """
        # Embedding model file
        self.embedding_model_path = os.path.join(MODELS, "discogs-effnet-bs64-1.pb")
        # Classification model file
        self.classification_model_path = os.path.join(MODELS, "mtg_jamendo_instrument-discogs-effnet-1.pb")
        # Metadata (genre classes, etc.)
        self.metadata_path = os.path.join(MODELS, "mtg_jamendo_instrument-discogs-effnet-1.json")

        # Load the metadata
        self.metadata = self._load_metadata()

        # Initialize both models
        self._initialize_models()

    def _load_metadata(self):
        if not os.path.exists(self.metadata_path):
            raise FileNotFoundError(f"Metadata file not found: {self.metadata_path}")

        with open(self.metadata_path, "r") as f:
            return json.load(f)

    def _initialize_models(self):
        # Check the files exist
        if not os.path.exists(self.embedding_model_path):
            raise FileNotFoundError(f"Embedding model not found: {self.embedding_model_path}")
        if not os.path.exists(self.classification_model_path):
            raise FileNotFoundError(f"Classification model not found: {self.classification_model_path}")

        # 1) Embedding model
        self.embedding_model = TensorflowPredictEffnetDiscogs(
            graphFilename=self.embedding_model_path,
            output="PartitionedCall:1"
        )

        # 2) Classification model (2D)
        self.classification_model = TensorflowPredict2D(
            graphFilename=self.classification_model_path
        )

    def load_audio(self, audio_file, sample_rate=16000):
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"Audio file not found: {audio_file}")
        loader = MonoLoader(filename=audio_file, sampleRate=sample_rate, resampleQuality=4)
        return loader()

    def classify_instruments(self, audio_file):
        # Load audio
        audio = self.load_audio(audio_file, sample_rate=16000)

        # Extract embeddings
        embeddings = self.embedding_model(audio)

        # Classify embeddings
        predictions = self.classification_model(embeddings)
        # If shape is [time, classes], average over time
        if predictions.ndim == 2:
            predictions = np.mean(predictions, axis=0)

        # Convert predictions to dictionary
        instrument_scores = {
            self.metadata["classes"][i]: predictions[i]
            for i in range(len(predictions))
        }

        # Sort instruments by score
        sorted_instruments = sorted(instrument_scores.items(), key=lambda x: x[1], reverse=True)

        # Find the jump in probabilities
        probabilities = [score for _, score in sorted_instruments]
        selected_instruments = []
        threshold_index = len(probabilities)

        # Detect the first significant drop in probability
        for i in range(1, len(probabilities)):
            if probabilities[i - 1] - probabilities[i] > 0.05:  # Adjust this threshold as needed
                threshold_index = i
                break

        # Always include instruments with scores above a minimum threshold (e.g., 0.2)
        min_threshold = 0.2
        selected_instruments = [
            instrument for instrument, score in sorted_instruments
            if score > min_threshold or sorted_instruments.index((instrument, score)) < threshold_index
        ]

        # Return the selected instruments
        return selected_instruments

def main():
    audio_file = "files/audio.wav"

    classifier = JamendoInstrumentClassifier()

    try:
        selected_instruments = classifier.classify_instruments(audio_file)

        # Print results
        print(f"Detected Instruments: {', '.join(selected_instruments)}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
