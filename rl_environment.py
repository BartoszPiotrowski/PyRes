from glob import glob

class Environment()
    def __init__(self, problems_dir, inferences_per_step):
        self.actions = ... # names / numbers of queues
        self.problem_files = glob(problems_dir + '/*.p')

        # TODO initialize the prover


    def step(self, action):
        state = self.current_state_characterization()
        # TODO make action
        reward = self.reward()
        done = self.done()
        # return state, reward, done

