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

class DiscogsGenreClassifier:
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
        print(f"MODELS environment variable: {MODELS}")

        self.embedding_model_path = os.path.join(MODELS, "discogs-effnet-bs64-1.pb")
        # Classification model file
        self.classification_model_path = os.path.join(MODELS, "genre_discogs400-discogs-effnet-1.pb")
        # Metadata (genre classes, etc.)
        self.metadata_path = os.path.join(MODELS, "genre_discogs400-discogs-effnet-1.json")
        
        print(f"Metadata file path: {self.metadata_path}")

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
            graphFilename=self.classification_model_path,
            input="serving_default_model_Placeholder",
            output="PartitionedCall:0"
        )

    def load_audio(self, audio_file, sample_rate=16000):
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"Audio file not found: {audio_file}")
        loader = MonoLoader(filename=audio_file, sampleRate=sample_rate, resampleQuality=4)
        return loader()

    def classify_genres(self, audio_file):
        """
        - Load audio at 16 kHz
        - Extract embeddings
        - Classify embeddings
        - Return main_genre, primary_genre, secondary_genre
        """
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

        # Extract main, primary, and secondary genres
        if len(sorted_genres) >= 2:
            primary_genre_full = sorted_genres[0][0]
            secondary_genre_full = sorted_genres[1][0]
            main_genre = primary_genre_full.split("---")[0]
            primary_genre = primary_genre_full.split("---")[1]
            secondary_genre = secondary_genre_full.split("---")[1]
        else:
            raise ValueError("Not enough genres predicted to determine main, primary, and secondary genres.")

        return main_genre, primary_genre, secondary_genre


def main():
    audio_file = "files/audio.wav"

    classifier = DiscogsGenreClassifier()
    print(f"Current working directory: {os.getcwd()}")
    try:
        main_genre, primary_genre, secondary_genre = classifier.classify_genres(audio_file)

        # Print results
        print(f"Main Genre: {main_genre}")
        print(f"Primary Genre: {primary_genre}")
        print(f"Secondary Genre: {secondary_genre}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
