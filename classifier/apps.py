from django.apps import AppConfig
from .pytorch_model.load import load_pretrained_model
from pathlib import Path
import torch

class ClassifierConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "classifier"

    def ready(self):
        """This method is called when the app is loaded"""
        model_path = Path(__file__).resolve().parent / "pytorch_model" / "weights" / "0.99_MNST_digit_classifier.pt"
        try:
            self.model = load_pretrained_model(model_path)
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None
