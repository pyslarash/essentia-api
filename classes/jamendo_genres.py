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

class JamendoGenreClassifier:
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
        self.classification_model_path = os.path.join(MODELS, "mtg_jamendo_genre-discogs-effnet-1.pb")
        # Metadata (genre classes, etc.)
        self.metadata_path = os.path.join(MODELS, "mtg_jamendo_genre-discogs-effnet-1.json")

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

    def classify_genres(self, audio_file):
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
        genre_scores = {
            self.metadata["classes"][i]: predictions[i]
            for i in range(len(predictions))
        }

        # Sort genres by score
        sorted_genres = sorted(genre_scores.items(), key=lambda x: x[1], reverse=True)

        # Extract the top 3 genres
        top_genres = sorted_genres[:3]  # Get the top 3 (if fewer, it will adapt)

        # Handle cases where fewer than 3 genres exist
        primary_genre = top_genres[0][0] if len(top_genres) > 0 else None
        secondary_genre = top_genres[1][0] if len(top_genres) > 1 else None
        tertiary_genre = top_genres[2][0] if len(top_genres) > 2 else None

        return primary_genre, secondary_genre, tertiary_genre

def main():
    audio_file = "files/audio.wav"

    classifier = JamendoGenreClassifier()

    try:
        primary_genre, secondary_genre, tertiary_genre = classifier.classify_genres(audio_file)

        # Print results
        print(f"Primary Genre: {primary_genre}")
        print(f"Secondary Genre: {secondary_genre}")
        print(f"Tertiary Genre: {tertiary_genre}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
