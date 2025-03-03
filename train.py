import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import numpy as np
import os
from model import MusicVideoGeneratorModel  # Assuming the model is defined in model.py

class MusicVideoDataset(Dataset):
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.data = self.load_data()

    def load_data(self):
        data = []
        for file in os.listdir(self.data_dir):
            if file.endswith('.npy'):
                data.append(np.load(os.path.join(self.data_dir, file)))
        return data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

def get_data_loaders(data_dir, batch_size=32, shuffle=True):
    dataset = MusicVideoDataset(data_dir)
    data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)
    return data_loader

def train_model(model, data_loader, criterion, optimizer, num_epochs=25):
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        for inputs in data_loader:
            inputs = inputs.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, inputs)
            loss.backward()
            optimizer.step()
            running_loss += loss.item() * inputs.size(0)

        epoch_loss = running_loss / len(data_loader.dataset)
        print(f'Epoch {epoch}/{num_epochs - 1}, Loss: {epoch_loss:.4f}')
    return model

def evaluate_model(model, data_loader, criterion):
    model.eval()
    running_loss = 0.0
    with torch.no_grad():
        for inputs in data_loader:
            inputs = inputs.to(device)
            outputs = model(inputs)
            loss = criterion(outputs, inputs)
            running_loss += loss.item() * inputs.size(0)

    total_loss = running_loss / len(data_loader.dataset)
    print(f'Evaluation Loss: {total_loss:.4f}')
    return total_loss

def save_model(model, path='music_video_generator.pth'):
    torch.save(model.state_dict(), path)

if __name__ == "__main__":
    data_dir = 'path/to/data'
    batch_size = 32
    num_epochs = 25
    learning_rate = 0.001

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    model = MusicVideoGeneratorModel().to(device)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    data_loader = get_data_loaders(data_dir, batch_size)

    trained_model = train_model(model, data_loader, criterion, optimizer, num_epochs)
    evaluate_model(trained_model, data_loader, criterion)
    save_model(trained_model)