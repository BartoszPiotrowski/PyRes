import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F


class PolicyNetwork(nn.Module):
    def __init__(self, num_features=None, num_actions=None,
                 num_hidden_layers=0, num_units=64, learning_rate=0.001):
        super(Net, self).__init__()
        self.num_hidden_layers = num_hidden_layers
        self.num_uits = num_units
        self.learning_rate = learning_rate
        self.layers = []
        self.layers.append(nn.Linear(num_features, num_units))
        for _ in range(self.num_hidden_layers)
            self.layers.append(nn.Linear(self.num_units, self.num_units))
        self.layers.append(nn.Linear(self.num_units, self.num_actions))

        self.optimizer = optim.SGD(self.parameters(), lr=self.learning_rate)

    def forward(self, x):
        for layer in self.layers:
            x = F.relu(layer(x))
        x = F.softmax(x)
        return x

    def train(self, batch):
        output = self.forward(...)
        target = ...
        loss = nn.MSELoss()(output, target)
        loss.backward()
        self.optimizer.zero_grad()
        self.optimizer.step()
