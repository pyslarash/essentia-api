import os
import numpy as np
from dotenv import load_dotenv
from essentia.standard import MonoLoader, TensorflowPredictVGGish, TensorflowPredict2D

load_dotenv()

MODELS = os.getenv('MODELS')

class DanceabilityClassifier:
    """
    Classifies the danceability of an audio file using VGGish embeddings.
    """

    def __init__(self):
        """
        model_dir should contain:
        - audioset-vggish-3.pb (embedding model)
        - danceability-audioset-vggish-1.pb (classification model)
        """
        # Paths to the models
        self.embedding_model_path = os.path.join(MODELS, "audioset-vggish-3.pb")
        self.classification_model_path = os.path.join(MODELS, "danceability-audioset-vggish-1.pb")

        # Initialize models
        self._initialize_models()

    def _initialize_models(self):
        # Check if model files exist
        if not os.path.exists(self.embedding_model_path):
            raise FileNotFoundError(f"Embedding model not found: {self.embedding_model_path}")
        if not os.path.exists(self.classification_model_path):
            raise FileNotFoundError(f"Classification model not found: {self.classification_model_path}")

        # Initialize the embedding model
        self.embedding_model = TensorflowPredictVGGish(
            graphFilename=self.embedding_model_path,
            output="model/vggish/embeddings"
        )

        # Initialize the danceability classification model
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

    def classify_danceability(self, audio_file):
        """
        Classifies the danceability of the given audio file.

        Returns:
            dict: A dictionary with danceability levels (`danceable` and `not_danceable`) and their probabilities.
        """
        # Load and process the audio
        audio = self.load_audio(audio_file, sample_rate=16000)

        # Extract embeddings
        embeddings = self.embedding_model(audio)

        # Get danceability predictions
        predictions = self.classification_model(embeddings)

        # If shape is [time, classes], average over time
        if predictions.ndim == 2:
            predictions = np.mean(predictions, axis=0)

        # Convert predictions to a dictionary
        classes = ["not_danceable", "danceable"]
        danceability_scores = {classes[i]: float(predictions[i]) for i in range(len(classes))}

        return danceability_scores


def main():
    audio_file = "files/audio.wav"

    classifier = DanceabilityClassifier()

    try:
        # Classify danceability
        danceability_scores = classifier.classify_danceability(audio_file)
        print("Danceability Scores:")
        for label, score in danceability_scores.items():
            print(f"  {label}: {score:.4f}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
