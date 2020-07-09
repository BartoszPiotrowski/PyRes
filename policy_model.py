import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
import os
from utils import read_lines, write_lines
from normalizer import Normalizer


class PolicyModel:
    def __init__(self, learning_rate=0.001, normalizer=None, save_path=None, **model_shape):
        self.save_path=save_path
        self.normalizer = normalizer
        if model_shape:
            self.model_shape = model_shape
            self.define_layers(**model_shape)
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

    def train(self, states, actions, returns):
        states = self.normalizer.normalize(states)
        states = torch.tensor(states, dtype=torch.float)
        actions = torch.tensor(actions, dtype=torch.long)
        returns = torch.tensor(returns, dtype=torch.float)
        actions_probs = self.model(states)
        selected_actions_probs = actions_probs[np.arange(len(actions)), actions]
        selected_actions_probs_log = torch.log(selected_actions_probs)
        loss = - torch.mean(returns * selected_actions_probs_log)
        # TODO clipping of the loss
        #print(loss.item())
        self.optimizer.zero_grad() # TODO right place?
        loss.backward()
        self.optimizer.step()
        return loss.item()

#        # test if loss decreases
#        actions_probs = self.model(states)
#        selected_actions_probs = actions_probs[np.arange(len(actions)), actions]
#        selected_actions_probs_log = torch.log(selected_actions_probs)
#        loss = - torch.mean(returns * selected_actions_probs_log)
#        print(loss)

    def predict(self, state): # input: a proof state vector
        batch_states = torch.Tensor(self.normalizer.normalize([state]))
        # when you use the line below, loss goes do down, but the reward too
        # and action 1 is much more frequent
        #batch_states = torch.Tensor([state])
        pred_tensor = self.model(batch_states)
        pred_numpy = pred_tensor.detach().numpy()[0]
        return pred_numpy

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
        write_lines(lines, path)


    def load_layers_definitions(self, path):
        param_dict = dict([(l.split(' ')[0], int(l.split(' ')[1])) \
                            for l in read_lines(path)])
        self.define_layers(**param_dict)


    def load(self, path): # we load a model for prediction only
        self.normalizer = Normalizer(load_from_file=path + '.norm')
        self.load_layers_definitions(path + '.meta')
        self.model.load_state_dict(torch.load(path))
        self.model.eval()


if __name__=='__main__':
    # TEST
    policy_model = PolicyModel(num_features=4,
                                   num_actions=2,
                                   num_hidden_layers=1,
                                   num_units=64,
                                   learning_rate=0.01)
    #batch_states = torch.Tensor([[1,2,3,4],[5,6,7,8]])
    state = [5,6,7,8]
    print(policy_model.model)
    #print(list(policy_model.model.parameters()))
    print(policy_model.predict(state))
    policy_model.save('tmp/policy_model.pt')

    policy_model = PolicyModel()
    policy_model.load('tmp/policy_model.pt')
    print(policy_model.predict(state))

