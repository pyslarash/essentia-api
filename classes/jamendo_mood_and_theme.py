import json
import os
import numpy as np
from dotenv import load_dotenv
from essentia.standard import MonoLoader, TensorflowPredictEffnetDiscogs, TensorflowPredict2D

load_dotenv()

MODELS = os.getenv('MODELS')

class JamendoMoodAndThemeClassifier:
    """
    Classifies the mood and theme of an audio file using the MTG-Jamendo dataset.
    """

    def __init__(self):
        """
        model_dir should contain:
        - discogs-effnet-bs64-1.pb (embedding model)
        - mtg_jamendo_moodtheme-discogs-effnet-1.pb (classification model)
        - mtg_jamendo_moodtheme-discogs-effnet-1.json (metadata file with class names)
        """
        # Paths to the models and metadata
        self.embedding_model_path = os.path.join(MODELS, "discogs-effnet-bs64-1.pb")
        self.classification_model_path = os.path.join(MODELS, "mtg_jamendo_moodtheme-discogs-effnet-1.pb")
        self.metadata_path = os.path.join(MODELS, "mtg_jamendo_moodtheme-discogs-effnet-1.json")

        # Initialize models and load metadata
        self._initialize_models()
        self._load_metadata()

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

        # Initialize the mood and theme classification model
        self.classification_model = TensorflowPredict2D(
            graphFilename=self.classification_model_path
        )

    def _load_metadata(self):
        # Check if metadata file exists
        if not os.path.exists(self.metadata_path):
            raise FileNotFoundError(f"Metadata file not found: {self.metadata_path}")

        # Load class names from the metadata
        with open(self.metadata_path, "r") as f:
            self.classes = json.load(f)["classes"]

    def load_audio(self, audio_file, sample_rate=16000):
        """
        Loads audio and resamples to the specified sample rate.
        """
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"Audio file not found: {audio_file}")
        loader = MonoLoader(filename=audio_file, sampleRate=sample_rate, resampleQuality=4)
        return loader()

    def classify_mood_and_theme(self, audio_file, top_n=3):
        """
        Classifies the mood and theme of the given audio file.

        Args:
            audio_file (str): Path to the audio file.
            top_n (int): Number of top predictions to return.

        Returns:
            list: A list of the top moods/themes by their labels.
        """
        # Load and process the audio
        audio = self.load_audio(audio_file, sample_rate=16000)

        # Extract embeddings
        embeddings = self.embedding_model(audio)

        # Get mood and theme predictions
        predictions = self.classification_model(embeddings)

        # If shape is [time, classes], average over time
        if predictions.ndim == 2:
            predictions = np.mean(predictions, axis=0)

        # Sort predictions by score in descending order
        sorted_predictions = sorted(
            [(self.classes[i], predictions[i]) for i in range(len(predictions))],
            key=lambda x: x[1],
            reverse=True
        )

        # Return only the top N labels
        top_labels = [label for label, _ in sorted_predictions[:top_n]]
        return top_labels

def main():
    audio_file = "files/audio.wav"

    classifier = JamendoMoodAndThemeClassifier()

    try:
        # Classify mood and theme and get top 3
        top_moods_and_themes = classifier.classify_mood_and_theme(audio_file, top_n=3)
        print("Top 3 Moods and Themes:")
        print(top_moods_and_themes)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
