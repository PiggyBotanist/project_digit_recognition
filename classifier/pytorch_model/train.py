from model import *
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from pathlib import Path
import torch
import sys


# Define parameters
learning_rate = 0.001
batch_size = 64
epochs = 10
seed = 40

# Define data location (downlaod if does not exist)
parent_folder = Path(__file__).resolve().parent
path_dataset = parent_folder / "data"
path_weights = parent_folder / "weights"

# Define output name
filename_weights = "MNST_digit_classifier"

# Set seed to ensure replication
torch.manual_seed(seed)

# Transform function (preprocessing)
transform = transforms.Compose([
    transforms.ToTensor(),                              # Convert image to tensor
    transforms.Normalize((0.5,), (0.5,)),               # Normalize to [-1, 1]
    transforms.Lambda(lambda x: torch.flatten(x))        # Flatten the image to 784
])

# Step 1: Load the data
train_dataset = datasets.MNIST(root=path_dataset, train=True, download=True, transform=transform)   # Load training data
test_dataset = datasets.MNIST(root=path_dataset, train=True, download=True, transform=transform)    # Load test data

# Step 2: Load the datasets into batches
train_loader = DataLoader(train_dataset, batch_size = batch_size, shuffle=True)                 # Convert to DataLoader
test_loader = DataLoader(test_dataset, batch_size = batch_size, shuffle=False)                  # Convert to DataLoader


# step 2: create and train the model
model = SimpleNN()
train_NN(model, train_loader, learning_rate, epochs)
accuracy = calculate_accuracy(model, test_loader)
print(f"Accuracy: {accuracy:.2f}%")

# Step 3: store the weights
save_weights(model, str(path_weights / filename_weights ))