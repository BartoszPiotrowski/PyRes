#!/bin/python3
"""
Reinforce algorithm for learning a queue (action) selection conditioned
on a proof state characterization.
"""


from sys import getsizeof
import numpy as np
from itertools import chain
from joblib import Parallel, delayed
from rl_environment import Environment
from policy_model import PolicyModel
from evaluate import evaluate
from returns import compute_returns
from problems import Problems
from utils import humanbytes, with_timeout, apply_temperature

if __name__ == "__main__":
    np.random.seed(42)

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "problems_list",
        type=str,
        help="Text file with a list of training problems.")
    parser.add_argument(
        "--inferences_per_step",
        default=10,
        type=int,
        help="Number of processed clauses treated as a one agent's step in "
             "the environment.")
    parser.add_argument(
        "--step_limit",
        default=100,
        type=int,
        help="Maximum number of (RL) steps per problem during training.")
    parser.add_argument(
        "--time_limit",
        default=10,
        type=int,
        help="Maximum number of (RL) steps per problem during training.")
    parser.add_argument(
        "--batch_size",
        default=16,
        type=int,
        help="Number of episodes forming one training batch of trajectories.")
    parser.add_argument(
        "--episodes",
        default=10000,
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
        default=0.99,
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
        "--temperature",
        default=1.1,
        type=float,
        help="""
        Float larger or equal than 1. When temperature = 1, action selection is
        governed by probabilities given by the policy model; values larger than
        1 make the selection more random (values > 10 make the selection almost
        uniform)
        """)
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
    parser.add_argument(
        "--n_jobs",
        default=0,
        type=int,
        help="Number of parallel jobs to run.")
    args = parser.parse_args()

    if not args.n_jobs:
        args.n_jobs = args.batch_size

    env = Environment(**vars(args))
    problems = Problems(**vars(args))

    policy_model = PolicyModel(
        num_features=env.num_state_features,
        num_actions=env.num_actions,
        num_hidden_layers=args.hidden_layers,
        num_units=args.units_in_hidden_layer,
        learning_rate=args.learning_rate,
        save_path=args.save_path)


    def generate_episodes(env, policy_model, problems, n_jobs):
        with Parallel(n_jobs=n_jobs) as parallel:
            trajectories_batch = parallel(
                delayed(generate_1_episode)(env, policy_model, problem) \
            for problem in problems)
        return trajectories_batch


    @with_timeout(args.time_limit)
    def generate_1_episode(env, policy_model, problem):
        try:
            #print(f"Generating episode with problem {problem}")
            env.load_problem(problem)
            states, actions, rewards, done = [], [], [], False
            state = env.state()
            while not done:
                action_probs = policy_model.predict(state)
                action_probs = apply_temperature(action_probs, args.temperature)
                action = np.random.choice(range(env.num_actions), p=action_probs)
                state, reward, done = env.step(action)
                states.append(state)
                rewards.append(reward)
                actions.append(action)
                #print(env.problem_path, env.steps_done, done)
            #print(humanbytes(getsizeof(states)))
            return zip(states, actions, rewards)
        except:
            return

    losses = []
    last_eval_epoch = -1
    generated_episodes = 0
    while generated_episodes < args.episodes:
        problems_batch = problems.next_batch()
        #print(f"Generating {len(problems_batch)} episodes with "
        #      f"{args.n_jobs} parallel jobs.")
        trajectories_batch = generate_episodes(env, policy_model,
                                               problems_batch, args.n_jobs)
        generated_episodes += len(trajectories_batch)
        trajectories_batch = [tb for tb in trajectories_batch if tb]
        trajectories_chain = chain(*trajectories_batch)
        states_batch, actions_batch, rewards_batch = zip(*trajectories_chain)
        returns_batch = compute_returns(rewards_batch, args.gamma)
        loss = policy_model.train(states_batch, actions_batch, returns_batch)
        print(loss)
        losses.append(loss)
        print(
              f'epoch: {problems.epoch:2d}    '
              f'episodes total: {problems.processed:4d}    '
              f'episodes batch: {len(trajectories_batch):3d}    '
              f'avg reward: {np.mean(rewards_batch):.2f}    '
              f'avg policy loss: {np.mean(losses):.2f}'
        )
        if problems.epoch - last_eval_epoch >= args.evaluate_each:
            last_eval_epoch = problems.epoch
            print('\nEvaluating policy model on training problems...')
            saved_policy_model = policy_model.save()
            evaluate(args.problems_list, args.pyres_options,
                     args.eval_timeout, saved_policy_model)
            print()


