"""
Reinforce algorithm for learning queue (action) selection conditioned
on proof state characterization.
"""


import numpy as np
from rl_environment import Environment
from policy_model import PolicyModel


if __name__ == "__main__":
    np.random.seed(42)

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--problems_dir",
        type=str)
    parser.add_argument(
        "--inferences_per_step",
        default=10,
        type=int,
        help="Number of processed clauses treated as a one agent's step in "
             "the environment.")
    parser.add_argument(
        "--batch_size",
        default=50,
        type=int)
    parser.add_argument(
        "--episodes", # 1 episode == 1 proof attempt for 1 problem
        default=100,
        type=int,
        help="Number of episodes to train on.")
    parser.add_argument(
        "--gamma",
        default=1.0,
        type=float,
        help="Discounting factor.")
    parser.add_argument(
        "--hidden_layers",
        default=100,
        type=int,
        help="Number of hidden layers.")
    parser.add_argument(
        "--units_in_hidden_layer",
        default=100,
        type=int,
        help="Size of hidden layer.")
    parser.add_argument(
        "--learning_rate",
        default=0.001,
        type=float,
        help="Learning rate.")
    args = parser.parse_args()


env = Environment(args.problems_dir, args.inferences_per_step)
policy_model = PolicyModel(
    num_features=env.num_state_features,
    num_actions=env.num_actions,
    num_hidden_layers=args.hidden_layers,
    num_units=args.units_in_hidden_layer,
    learning_rate=args.learning_rate)

while True:
    batch_states, batch_actions, batch_returns = [], [], []
    for _ in range(batch_size):
        states, actions, rewards, done = [], [], [], False
        # TODO 'done' == one problem tried, right?
        # TODO maybe parallel processing
        while not done:
            action_distr = policy_model.predict(state)
            action = np.random.choice(range(env.actions), p=action_distr)
            state, reward, done = env.step(action)
            states.append(state)
            rewards.append(reward)
            actions.append(action)
            # TODO controll if there is no mess because of removing next_state

        returns = []
        sum_of_rewards = 0
        rewards.reverse()
        for r in rewards:
            sum_of_rewards = args.gamma * sum_of_rewards + r
            returns.append(sum_of_rewards)
        returns.reverse()

        batch_states.extend(states)
        batch_actions.extend(actions)
        batch_returns.extend(returns)

    policy_model.train(batch_states, batch_actions, batch_returns)
