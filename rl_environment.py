import os
from glob import glob
from random import shuffle, choice
from fofspec import FOFSpec
from saturation import ProofState
from process_pyres_options import processPyresOptions
from utils import read_lines


class Environment:
    def __init__(self,
                 inferences_per_step=100,
                 step_limit=100,
                 pyres_options=None,
                 **kwargs):
        self.pyres_options = processPyresOptions(pyres_options)
        self.inferences_per_step = inferences_per_step
        self.step_limit = step_limit
        self.problem = None
        self.problem_path = None
        self.proof_state = None
        self.steps_done = 0
        self.done = False
        self.load_problem('Problems/PUZ/PUZ001+1.p')
        # the above is just to initialize what is below (temporary solution)
        self.num_actions = self.proof_state.num_eval_functions
        self.num_state_features = len(self.proof_state.proof_state_vector)


    def load_problem(self, problem_path):
        self.problem_path = problem_path
        #print(f'Current training problem: {self.problem_path} ...')
        problem = FOFSpec()
        problem.parse(self.problem_path)
        if not self.pyres_options['suppressEqAxioms']:
            problem.addEqAxioms()
        self.problem = problem.clausify()
        self.proof_state = ProofState(self.pyres_options['main'],
                                      self.problem, True,
                                      self.pyres_options['indexed'], True)


    def step(self, action):
        self.steps_done += 1
        state = self.state()
        if self.steps_done > self.step_limit:
            #print(f'Step limit reached. Problem not solved.')
            #print(self.proof_state.statisticsStr())
            reward, done = 0, True
        else:
            for _ in range(self.inferences_per_step):
                try:
                    res = self.proof_state.processClause(action)
                    if res != None: # empty clause found = proof found
                        #print(f'Solved!')
                        #print(self.proof_state.statisticsStr())
                        reward, done = 1, True
                        break
                except:
                    print('Error while processing a clause; problem '
                          f'{self.problem_path}')
                    reward, done = 0, True
                    break
            else:
                reward, done = 0, False
        return state, reward, done


    def state(self):
        return self.proof_state.proof_state_vector


if __name__=='__main__':
    env = Environment(pyres_options='-tfb -nsmallest')
    env.load_problem('Problems/ALG/ALG171+1.p')
    for _ in range(3):
        i = choice(range(env.num_actions))
        env.step(i)
