import os
import numpy as np
from dotenv import load_dotenv
from essentia.standard import MonoLoader, TensorflowPredictEffnetDiscogs, TensorflowPredict2D

load_dotenv()

MODELS = os.getenv('MODELS')

class TimbreClassifier:
    """
    Classifies the timbre of an audio file into `bright` or `dark`.
    """

    def __init__(self):
        """
        model_dir should contain:
        - discogs-effnet-bs64-1.pb (embedding model)
        - timbre-discogs-effnet-1.pb (classification model)
        """
        # Paths to the models
        self.embedding_model_path = os.path.join(MODELS, "discogs-effnet-bs64-1.pb")
        self.classification_model_path = os.path.join(MODELS, "timbre-discogs-effnet-1.pb")

        # Initialize models
        self._initialize_models()

    def _initialize_models(self):
        # Check if model files exist
        if not os.path.exists(self.embedding_model_path):
            raise FileNotFoundError(f"Embedding model not found: {self.embedding_model_path}")
        if not os.path.exists(self.classification_model_path):
            raise FileNotFoundError(f"Classification model not found: {self.classification_model_path}")

        # Initialize the embedding model
        self.embedding_model = TensorflowPredictEffnetDiscogs(
            graphFilename=self.embedding_model_path,
            output="PartitionedCall:1"
        )

        # Initialize the timbre classification model
        self.classification_model = TensorflowPredict2D(
            graphFilename=self.classification_model_path,
            output="model/Softmax"
        )

    def load_audio(self, audio_file, sample_rate=16000):
        """
        Loads audio and resamples to the specified sample rate.
        """
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"Audio file not found: {audio_file}")
        loader = MonoLoader(filename=audio_file, sampleRate=sample_rate, resampleQuality=4)
        return loader()

    def classify_timbre(self, audio_file):
        """
        Classifies the timbre of the given audio file.

        Returns:
            dict: A dictionary with probabilities for `bright` and `dark`.
        """
        # Load and process the audio
        audio = self.load_audio(audio_file, sample_rate=16000)

        # Extract embeddings
        embeddings = self.embedding_model(audio)

        # Get timbre predictions
        predictions = self.classification_model(embeddings)

        # If shape is [time, classes], average over time
        if predictions.ndim == 2:
            predictions = np.mean(predictions, axis=0)

        # Define class labels
        classes = ["bright", "dark"]

        # Convert predictions to a dictionary
        timbre_scores = {classes[i]: float(predictions[i]) for i in range(len(classes))}

        return timbre_scores


def main():
    audio_file = "files/audio.wav"

    classifier = TimbreClassifier()

    try:
        # Classify timbre
        timbre_scores = classifier.classify_timbre(audio_file)
        print("Timbre Scores:")
        for label, score in timbre_scores.items():
            print(f"  {label}: {score:.4f}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
