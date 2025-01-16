import os
import numpy as np
from dotenv import load_dotenv
from essentia.standard import MonoLoader, TensorflowPredictMusiCNN, TensorflowPredict2D

load_dotenv()

MODELS = os.getenv('MODELS')

class ArousalValenceEmomusicMusiCNNClassifier:
    """
    Classifies the arousal and valence of an audio file.
    """

    def __init__(self):
        """
        model_dir should contain:
        - msd-musicnn-1.pb (embedding model)
        - deam-msd-musicnn-2.pb (classification model)
        """
        # Paths to the models
        self.embedding_model_path = os.path.join(MODELS, "msd-musicnn-1.pb")
        self.classification_model_path = os.path.join(MODELS, "deam-msd-musicnn-2.pb")

        # Initialize models
        self._initialize_models()

    def _initialize_models(self):
        # Check if model files exist
        if not os.path.exists(self.embedding_model_path):
            raise FileNotFoundError(f"Embedding model not found: {self.embedding_model_path}")
        if not os.path.exists(self.classification_model_path):
            raise FileNotFoundError(f"Classification model not found: {self.classification_model_path}")

        # Initialize the embedding model
        self.embedding_model = TensorflowPredictMusiCNN(
            graphFilename=self.embedding_model_path,
            output="model/dense/BiasAdd"
        )

        # Initialize the arousal/valence classification model
        self.classification_model = TensorflowPredict2D(
            graphFilename=self.classification_model_path,
            output="model/Identity"
        )

    def load_audio(self, audio_file, sample_rate=16000):
        """
        Loads audio and resamples to the specified sample rate.
        """
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"Audio file not found: {audio_file}")
        loader = MonoLoader(filename=audio_file, sampleRate=sample_rate, resampleQuality=4)
        return loader()

    def classify_arousal_valence(self, audio_file):
        """
        Classifies the arousal and valence of the given audio file.

        Returns:
            dict: A dictionary with arousal and valence scores normalized between 0 and 1.
        """
        # Load and process the audio
        audio = self.load_audio(audio_file, sample_rate=16000)

        # Extract embeddings
        embeddings = self.embedding_model(audio)

        # Get arousal/valence predictions
        predictions = self.classification_model(embeddings)

        # If shape is [time, classes], average over time
        if predictions.ndim == 2:
            predictions = np.mean(predictions, axis=0)

        # Normalize predictions from the range [1, 9] to [0, 1]
        normalized_predictions = (predictions - 1) / (9 - 1)

        # Convert normalized predictions to a dictionary
        arousal_valence_scores = {
            "arousal": float(normalized_predictions[0]),  # Arousal score
            "valence": float(normalized_predictions[1])  # Valence score
        }

        return arousal_valence_scores

def main():
    audio_file = "files/audio.wav"

    classifier = ArousalValenceEmomusicMusiCNNClassifier()

    try:
        # Classify arousal and valence
        arousal_valence_scores = classifier.classify_arousal_valence(audio_file)
        print("Arousal and Valence Scores:")
        for label, score in arousal_valence_scores.items():
            print(f"  {label.capitalize()}: {score:.4f}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
