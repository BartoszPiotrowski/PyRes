import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
import os
from utils import read_lines, write_lines


class PolicyModel:
    def __init__(self, learning_rate=0.001, **model_shape):
        if model_shape:
            self.model_shape = model_shape
            self.define_layers(**model_shape)
            self.loss = nn.MSELoss()
            self.learning_rate = learning_rate
            self.optimizer = optim.SGD(self.model.parameters(),
                                       lr=self.learning_rate)

    def define_layers(self,
                      num_features=None,
                      num_actions=None,
                      num_hidden_layers=0,
                      num_units=64):
        hidden_layers = []
        for _ in range(num_hidden_layers):
            hidden_layers.append(nn.Linear(num_units, num_units))
            hidden_layers.append(nn.ReLU())
        self.model = nn.Sequential(
            nn.Linear(num_features, num_units),
            nn.ReLU(),
            *hidden_layers,
            nn.Linear(num_units, num_actions),
            nn.Softmax(dim=1)
        )

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

    def save(self, path):
        dirpath = os.path.dirname(path)
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        torch.save(self.model.state_dict(), path)
        self.save_layers_definitions(path + '.meta')


    def save_layers_definitions(self, path):
        lines = [' '.join([p, str(self.model_shape[p])]) \
                 for p in self.model_shape]
        write_lines(lines, path)


    def load_layers_definitions(self, path):
        param_dict = dict([(l.split(' ')[0], int(l.split(' ')[1])) \
                            for l in read_lines(path)])
        self.define_layers(**param_dict)


    def load(self, path): # we load a model for prediction only
        self.load_layers_definitions(path + '.meta')
        self.model.load_state_dict(torch.load(path))
        self.model.eval()


if __name__=='__main__':
    policy_model = PolicyModel(num_features=4,
                                   num_actions=3,
                                   num_hidden_layers=1,
                                   num_units=64,
                                   learning_rate=0.01)
    batch_states = torch.Tensor([[1,2,3,4],[5,6,7,8]])
    print(policy_model.model)
    #print(list(policy_model.model.parameters()))
    print(policy_model.predict(batch_states))
    policy_model.save('tmp/saved_model.pt')

    policy_model = PolicyModel()
    policy_model.load('tmp/saved_model.pt')
    print(policy_model.predict(batch_states))

