from glob import glob
from random import shuffle, choice
from fofspec import FOFSpec
from saturation import ProofState
from process_pyres_options import processPyresOptions


class Environment:
    def __init__(self,
                 problems_dir=None,
                 inferences_per_step=10,
                 pyres_options=None):
        self.pyres_options = processPyresOptions(pyres_options)
        self.inferences_per_step = inferences_per_step
        self.problems = glob(problems_dir + '/*.p')
        shuffle(self.problems)
        self.current_problem_index = -1
        self.current_problem_path = None
        self.current_problem = None
        self.proof_state = None
        self.epoch = 0
        self.done = False
        self.load_next_problem()
        self.num_actions = self.proof_state.num_eval_functions
        self.num_state_features = len(self.proof_state.proof_state_vector)


    def load_next_problem(self):
        self.current_problem_index += 1
        if not self.current_problem_index < len(self.problems):
            self.current_problem_index = 0
            shuffle(self.problems)
            self.epoch += 1
        self.current_problem_path = \
            self.problems[self.current_problem_index]
        problem = FOFSpec()
        problem.parse(self.current_problem_path)
        if not self.pyres_options['suppressEqAxioms']:
            problem.addEqAxioms()
        self.current_problem = problem.clausify()
        self.proof_state = ProofState(self.pyres_options['main'],
                                      self.current_problem, True,
                                      self.pyres_options['indexed'])
        self.done = False


    def step(self, action):
        state = self.proof_state.proof_state_vector
        for _ in range(self.inferences_per_step):
            res = self.proof_state.processClause(action)
            if res != None: # empty clause found
                print(f'Problem {self.current_problem_path} solved.')
                print(self.proof_state.statisticsStr())
                reward, done = 1, True
                self.load_next_problem()
                return state, reward, done
        reward, done = 0, False
        return state, reward, done


if __name__=='__main__':
    env = Environment(problems_dir='EXAMPLES/ALG',
                      pyres_options='-tfb -nsmallest')
    while env.epoch < 3:
        i = choice(range(env.num_actions))
        env.step(i)
