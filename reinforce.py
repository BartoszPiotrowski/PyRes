"""
Reinforce algorithm for learning queue (action) selection conditioned
on proof state characterization.
"""


import numpy as np
from rl_environment import Environment
from policy_network import PolicyNetwork


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
        help="Number of processed clauses treated as one step in environment.")
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
        "--units_in_layer",
        default=100,
        type=int,
        help="Size of hidden layer.")
    parser.add_argument(
        "--hidden_layers",
        default=100,
        type=int,
        help="Number of hidden layers.")
    parser.add_argument(
        "--learning_rate",
        default=0.001,
        type=float,
        help="Learning rate.")
    args = parser.parse_args()


env = Environment(args.problems_dir, args.inferences_per_step)
policy_network = PolicyNetwork(args.hidden_layers, args.units_in_layer)

while True:
    batch_states, batch_actions, batch_returns = [], [], []
    for _ in range(batch_size):
        states, actions, rewards, done = [], [], [], False
        # TODO 'done' == one problem tried, right?
        # TODO maybe parallel processing
        while not done:
            action_distr = policy_network.predict(state)
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

    policy_network.train(batch_states, batch_actions, batch_returns)
