import os
import json
import numpy as np
from dotenv import load_dotenv
from essentia.standard import MonoLoader, TensorflowPredictVGGish

load_dotenv()

MODELS = os.getenv('MODELS')

class YamNetAudioEventClassifier:
    """
    Classifies audio events and extracts embeddings using YamNet.
    """

    def __init__(self):
        """
        model_dir should contain:
        - audioset-yamnet-1.pb (classification model)
        - yamnet_classes.json (metadata, including "classes")
        """
        # Classification model file
        self.classification_model_path = os.path.join(MODELS, "audioset-yamnet-1.pb")
        # Metadata (event classes, etc.)
        self.metadata_path = os.path.join(MODELS, "audioset-yamnet-1.json")

        # Load the metadata
        self.metadata = self._load_metadata()

        # Initialize the model
        self._initialize_model()

    def _load_metadata(self):
        if not os.path.exists(self.metadata_path):
            raise FileNotFoundError(f"Metadata file not found: {self.metadata_path}")

        with open(self.metadata_path, "r") as f:
            return json.load(f)

    def _initialize_model(self):
        # Check the file exists
        if not os.path.exists(self.classification_model_path):
            raise FileNotFoundError(f"Classification model not found: {self.classification_model_path}")

        # Initialize the classification model
        self.classification_model = TensorflowPredictVGGish(
            graphFilename=self.classification_model_path,
            input="melspectrogram",
            output="activations"
        )

    def load_audio(self, audio_file, sample_rate=16000):
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"Audio file not found: {audio_file}")
        loader = MonoLoader(filename=audio_file, sampleRate=sample_rate, resampleQuality=4)
        return loader()

    def classify_audio_events(self, audio_file):
        """
        Classifies audio events using YamNet.

        Returns:
            list: The top audio event classes detected.
        """
        # Load audio
        audio = self.load_audio(audio_file, sample_rate=16000)

        # Make predictions
        predictions = self.classification_model(audio)

        # If shape is [time, classes], average over time
        if predictions.ndim == 2:
            predictions = np.mean(predictions, axis=0)

        # Convert predictions to dictionary
        event_scores = {
            self.metadata["classes"][i]: predictions[i]
            for i in range(len(predictions))
        }

        # Sort events by score
        sorted_events = sorted(event_scores.items(), key=lambda x: x[1], reverse=True)

        # Return the top 5 events
        return [event for event, score in sorted_events[:10]]

def main():
    audio_file = "files/audio.wav"

    classifier = YamNetAudioEventClassifier()

    try:
        # Classify audio events
        detected_events = classifier.classify_audio_events(audio_file)
        print(f"Detected Audio Events: {', '.join(detected_events)}")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()