#!/bin/python3
"""
Random queue selection; for statistics collection.
"""


import numpy as np
from sys import getsizeof
from itertools import chain
from joblib import Parallel, delayed
from rl_environment import Environment
from problems import Problems
from utils import humanbytes, with_timeout, append_line


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
        "--n_jobs",
        default=0,
        type=int,
        help="Number of parallel jobs to run.")
    parser.add_argument(
        "--save_states",
        default='states.csv',
        type=str,
        help="Path to save recorded states.")
    args = parser.parse_args()

    if not args.n_jobs:
        args.n_jobs = args.batch_size

    env = Environment(**vars(args))
    problems = Problems(**vars(args))

    def generate_episodes(env, problems, n_jobs):
        with Parallel(n_jobs=n_jobs) as parallel:
            trajectories_batch = parallel(
                delayed(generate_1_episode)(env, problem) \
            for problem in problems)
        return trajectories_batch


    @with_timeout(args.time_limit)
    def generate_1_episode(env, problem):
        try:
            #print(f"Generating episode with problem {problem}")
            env.load_problem(problem)
            states, actions, rewards, done = [], [], [], False
            state = env.state()
            while not done:
                action = np.random.choice(range(env.num_actions))
                state, reward, done = env.step(action)
                states.append(state)
                rewards.append(reward)
                actions.append(action)
                #print(env.problem_path, env.steps_done, done)
            #print(humanbytes(getsizeof(states)))
            return zip(states, actions, rewards)
        except:
            return

    generated_episodes = 0
    while generated_episodes < args.episodes:
        problems_batch = problems.next_batch()
        #print(f"Generating {len(problems_batch)} episodes with "
        #      f"{args.n_jobs} parallel jobs.")
        trajectories_batch = generate_episodes(env, problems_batch, args.n_jobs)
        trajectories_batch = [tb for tb in trajectories_batch if tb]
        generated_episodes += len(trajectories_batch)
        trajectories_chain = chain(*trajectories_batch)
        states_batch, actions_batch, rewards_batch = zip(*trajectories_chain)
        for s in states_batch:
            append_line(','.join([str(i) for i in s]), args.save_states)
        #print(states_batch)
        #print(actions_batch)
        #print(returns_batch)
        #print(loss)
        print(
              f'epoch: {problems.epoch:2d}    '
              f'episodes total: {generated_episodes:4d}    '
              f'episodes batch: {len(trajectories_batch):3d}    '
              f'avg reward: {np.mean(rewards_batch):.2f}    '
        )

