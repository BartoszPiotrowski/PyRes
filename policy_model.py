import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
import os
from utils import read_lines, write_lines, apply_temperature
from normalizer import Normalizer


class PolicyModel:
    def __init__(self, learning_rate=None, temperature=None, optimizer=None,
                 activation=None, normalizer=None, save_path=None,
                 **model_shape):
        if model_shape:
            self.model_shape=model_shape
            self.optimizer=optimizer
            self.activation=activation
            self.temperature=temperature
            self.save_path=save_path
            self.normalizer = normalizer
            self.model = self.make_model(activation=activation, **model_shape)
            self.optimizer = {
                'Adam':optim.Adam(self.model.parameters(), lr=learning_rate),
                'SGD':optim.SGD(self.model.parameters(), lr=learning_rate)
            }[optimizer]


    def make_model(self, num_features=None, num_actions=None,
                   num_hidden_layers=0, num_units=0, activation=None):
        activation_fun = {
            'ReLU': nn.ReLU(),
            'Sigmoid': nn.Sigmoid()
        }[activation]
        hidden_layers = []
        for _ in range(num_hidden_layers):
            hidden_layers.append(nn.Linear(num_units, num_units))
            hidden_layers.append(activation_fun)
        return nn.Sequential(
            nn.Linear(num_features, num_units),
            activation_fun,
            *hidden_layers,
            nn.Linear(num_units, num_actions),
            nn.Softmax(dim=1)
        )


    def train(self, states, actions, returns):
        states = self.normalizer.normalize(states)
        states = torch.tensor(states, dtype=torch.float)
        actions = torch.tensor(actions, dtype=torch.long)
        returns = torch.tensor(returns, dtype=torch.float)
        actions_probs = self.model(states)
        selected_actions_probs = actions_probs[np.arange(len(actions)), actions]
        selected_actions_probs_log = torch.log(selected_actions_probs)
        loss = - torch.mean(returns * selected_actions_probs_log)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        return loss.item()


    def predict(self, state, policy_mode): # input: a proof state vector
        batch_states = torch.Tensor(self.normalizer.normalize([state]))
        probs_tensor = self.model(batch_states)
        probs_numpy = probs_tensor.detach().numpy()[0]
        action = self.probs_to_action(probs_numpy, policy_mode)
        return action


    def probs_to_action(self, probs, policy_mode):
        return {
            'stochastic': np.random.choice(range(len(probs)), p=probs),
            'semi-deterministic': self.semi_deterministic(probs, 5),
            'deterministic': np.argmax(probs)
        }[policy_mode]


    def semi_deterministic(self, probs, param):
        probs = np.multiply(param, probs)
        probs_softmax = np.exp(probs) / sum(np.exp(probs))
        action = np.random.choice(range(len(probs)), p=probs_softmax)
        return action


    def save(self, path=None):
        if path == None:
            path = self.save_path
        dirpath = os.path.dirname(path)
        if not os.path.exists(dirpath) and dirpath:
            os.makedirs(dirpath)
        torch.save(self.model.state_dict(), path)
        self.save_layers_definitions(path + '.meta')
        self.normalizer.save(path + '.norm')
        return path


    def save_layers_definitions(self, path):
        lines = [' '.join([p, str(self.model_shape[p])]) \
                 for p in self.model_shape]
        lines.append(f'activation {self.activation}')
        write_lines(lines, path)


    def load_layers_definitions(self, path):
        param_dict = dict([(l.split(' ')[0], l.split(' ')[1]) \
                            for l in read_lines(path)])
        for p in param_dict:
            try:
                param_dict[p] = int(param_dict[p])
            except:
                pass
        self.model = self.make_model(**param_dict)


    def load(self, path): # we load a model for prediction only
        self.normalizer = Normalizer(load_from_file=path + '.norm')
        self.load_layers_definitions(path + '.meta')
        self.model.load_state_dict(torch.load(path))
        self.model.eval()

    def __str__(self):
        return ('\n'
        'Policy model:\n'
        f'{self.model}\n\n'
        'Optimizer:\n'
        f'{self.optimizer}\n')



if __name__=='__main__':
    # TEST
    normalizer = Normalizer('data/states_rand_B3.csv', 'min_max')
    policy_model = PolicyModel(num_features=4,
                               num_actions=2,
                               num_hidden_layers=1,
                               num_units=64,
                               activation='ReLU',
                               optimizer='Adam',
                               normalizer=normalizer,
                               learning_rate=0.01)
    #batch_states = torch.Tensor([[1,2,3,4],[5,6,7,8]])
    state = [5,6,7,8]
    #print(list(policy_model.model.parameters()))
    print(policy_model.predict(state, policy_mode='deterministic'))
    policy_model.save('tmp/policy_model.pt')

    print(111)
    policy_model = PolicyModel()
    print(222)
    policy_model.load('tmp/policy_model.pt')
    print(policy_model.predict(state, policy_mode='deterministic'))

