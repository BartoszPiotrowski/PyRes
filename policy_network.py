import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np


class PolicyNetwork:
    def __init__(self, num_features=None, num_actions=None,
                 num_hidden_layers=0, num_units=64, learning_rate=0.001):
        layers = []
        layers.append(nn.Linear(num_features, num_units))
        layers.append(nn.ReLU())
        for _ in range(num_hidden_layers):
            layers.append(nn.Linear(num_units, num_units))
            layers.append(nn.ReLU())
        layers.append(nn.Linear(num_units, num_actions))
        layers.append(nn.Softmax(dim=1))
        self.model = nn.Sequential(*layers)
        self.learning_rate = learning_rate
        self.loss = nn.MSELoss()
        self.optimizer = optim.SGD(self.model.parameters(),
                                   lr=self.learning_rate)

    def train(self, batch_states, batch_actions, batch_returns):
        batch_states = torch.Tensor(batch_states)
        batch_actions = torch.Tensor(batch_actions)
        batch_returns = torch.Tensor(batch_returns)
        predicted_actions = self.model(batch_states)
        # TODO use returns, add logarithm
        self.loss(predicted_actions, batch_actions)
        self.loss.backward()
        self.optimizer.zero_grad()
        self.optimizer.step()

    def predict(self, batch_states):
        batch_states = torch.Tensor(batch_states)
        return self.model(batch_states)


if __name__=='__main__':
    policy_network = PolicyNetwork(4, 3, 1, 64, 0.01)
    batch_states = [[1,2,3,4],[5,6,7,8]]
    batch_states = torch.Tensor(batch_states)
    print(policy_network.model)
    #print(list(policy_network.model.parameters()))
    actions = policy_network.predict(batch_states)
    print(actions)

