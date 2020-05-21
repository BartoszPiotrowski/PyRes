"""
Reinforce algorithm for learning a queue (action) selection conditioned
on a proof state characterization.
"""


import numpy as np
from rl_environment import Environment
from policy_model import PolicyModel
from evaluate import evaluate
from returns import compute_returns


if __name__ == "__main__":
    np.random.seed(42)

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "problems_dir",
        type=str,
        help="Directory with training problems.")
    parser.add_argument(
        "--inferences_per_step",
        default=100,
        type=int,
        help="Number of processed clauses treated as a one agent's step in "
             "the environment.")
    parser.add_argument(
        "--step_limit",
        default=100,
        type=int,
        help="Maximum number of (RL) steps per problem during training.")
    parser.add_argument(
        "--batch_size",
        default=10,
        type=int,
        help="Number of episodes forming one training batch of trajectories.")
    parser.add_argument(
        "--episodes",
        default=100,
        type=int,
        help="Number of episodes to train on. "
             "(1 episode == 1 proof attempt for 1 problem.)")
    parser.add_argument(
        "--evaluate_each",
        default=10,
        type=int,
        help="After this number of training batches run evaluation with the "
             "current policy model.")
    parser.add_argument(
        "--gamma",
        default=1.0,
        type=float,
        help="Discounting factor.")
    parser.add_argument(
        "--hidden_layers",
        default=2,
        type=int,
        help="Number of hidden layers.")
    parser.add_argument(
        "--units_in_hidden_layer",
        default=100,
        type=int,
        help="Size of hidden layer.")
    parser.add_argument(
        "--learning_rate",
        default=0.01,
        type=float,
        help="Learning rate.")
    parser.add_argument(
        "--pyres_options",
        default='-tfb -nsmallest',
        type=str,
        help="String of options as for pyres-fof.py except of "
             "--given-clause-heuristic parameter (-H).")
    parser.add_argument(
        "--eval_timeout",
        default=10,
        type=float,
        help="Timeout for running PyRes with trained policy for one problem.")
    parser.add_argument(
        "--save_path",
        default='policy_model.pt',
        type=str,
        help="Path for saving a trained policy model.")
    args = parser.parse_args()


    env = Environment(**vars(args))

    policy_model = PolicyModel(
        num_features=env.num_state_features,
        num_actions=env.num_actions,
        num_hidden_layers=args.hidden_layers,
        num_units=args.units_in_hidden_layer,
        learning_rate=args.learning_rate,
        save_path=args.save_path)

    losses = []
    while env.episode < args.episodes:
        batch_states, batch_actions, batch_returns = [], [], []
        for i in range(args.batch_size):
            states, actions, rewards, done = [], [], [], False
            state = env.state()
            while not done:
                action_probs = policy_model.predict(state)
                action = np.random.choice(range(env.num_actions), p=action_probs)
                state, reward, done = env.step(action)
                states.append(state)
                rewards.append(reward)
                actions.append(action)

            returns = compute_returns(rewards, args.gamma)

            batch_states.extend(states)
            batch_actions.extend(actions)
            batch_returns.extend(returns)

        loss = policy_model.train(batch_states, batch_actions, batch_returns)
        losses.append(loss)
        if i % args.evaluate_each:
            print()
            print(f'Global step                         : {env.global_step}')
            print(f'Average policy model loss           : {np.mean(losses):.3f}')
            print('Evaluating policy model on training problems...')
            saved_policy_model = policy_model.save()
            evaluate(args.problems_dir, args.pyres_options,
                     args.eval_timeout, saved_policy_model)

