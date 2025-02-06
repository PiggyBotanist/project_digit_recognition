from django.apps import AppConfig
#from ..classifier.load import load_pretrained_model
from pathlib import Path


class FrontendConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "frontend"