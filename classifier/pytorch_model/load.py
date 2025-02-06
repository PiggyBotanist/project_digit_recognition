from .model import SimpleNN
import torch

# Load weights to our model
def load_pretrained_model(filepath: str):
    model = SimpleNN()
    model.load_state_dict(torch.load(filepath, weights_only=True))
    model.eval()
    return model