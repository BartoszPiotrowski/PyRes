import numpy as np
from utils import read_lines

class Problems:
    def __init__(self, problems_list=None, batch_size=None, **kwargs):
        self.epoch = 0
        self.epoch_finished = False
        self.processed = 0
        self.batch_size = batch_size
        self.problems = read_lines(problems_list)
        self._permutation = np.random.permutation(len(self.problems))

    def next_batch(self):
        if self.epoch_finished:
            self._permutation = np.random.permutation(len(self.problems))
            self.epoch += 1
            self.epoch_finished = False
        batch_size = min(self.batch_size, len(self._permutation))
        batch_indices = self._permutation[:batch_size]
        self._permutation = self._permutation[batch_size:]
        self.processed += batch_size
        if len(self._permutation) == 0:
            self.epoch_finished = True
        return [self.problems[i] for i in batch_indices]
