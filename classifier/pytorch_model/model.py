import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset
import matplotlib.pyplot as plt

# A very basic neural network that works really well with MNST numbers
class SimpleNN(nn.Module):
    def __init__(self, input_size=784, hidden_size=128, output_size=10):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)   # First hidden layer
        self.fc2 = nn.Linear(hidden_size, hidden_size)  # Second hidden layer
        self.fc3 = nn.Linear(hidden_size, hidden_size)  # Second hidden layer
        self.fc4 = nn.Linear(hidden_size, output_size)  # Output layer

    def forward(self, x):
        x = F.relu(self.fc1(x))                         # Activation function for hidden layer 1
        x = F.relu(self.fc2(x))                         # Activation function for hidden layer 2
        x = F.relu(self.fc3(x))                         # Activation function for hidden layer 3
        x = self.fc4(x)                                 # No activation, since CrossEntropyLoss expects raw scores
        return x

def train_NN(model: SimpleNN, dataset: DataLoader, learning_rate: float = 0.01, epochs: int = 5):
    # Initialize loss function and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    # Training loop
    for epoch in range(epochs):
        for batch_X, batch_y in dataset:
            optimizer.zero_grad()                       # Reset gradients
            outputs = model(batch_X)                    # Forward pass
            loss = criterion(outputs, batch_y)          # Compute loss
            loss.backward()                             # Backpropagation
            optimizer.step()                            # Update weights
        print(f"Epoch {epoch+1}/{epochs}, Loss: {loss.item():.4f}")

def calculate_accuracy(model: SimpleNN, dataset: DataLoader):
    model.eval()
    correct = 0
    total = 0

    with torch.no_grad():
        for batch_X, batch_y in dataset:
            outputs = model(batch_X.view(-1, 28*28))
            _, predicted = torch.max(outputs, 1)
            total += batch_y.size(0)
            correct += (predicted == batch_y).sum().item()

    accuracy = 100 * correct / total
    return accuracy

def save_weights(model: SimpleNN, path: str):
    torch.save(model.state_dict(), path)

def save_model_and_weights(model: SimpleNN, path: str):
    torch.save(model, path)