import numpy as np
from utils import read_lines, write_line, append_line


def z_score_norm(value, mean, std):
    return (value - mean) / std


def min_max_norm(value, min, max):
    return (value - min) / (max - min)


def stats_of_sample(sample_file):
    lines = read_lines(sample_file)
    lines = [[float(e) for e in l.split(',')] for l in lines]
    n_columns = len(lines[0])
    columns = [[l[i] for l in lines] for i in range(n_columns)]
    columns_stats = [{'min': min(c),
                      'max': max(c),
                      'mean': np.mean(c),
                      'std': np.std(c)}
                    for c in columns]
    return columns_stats


class Normalizer:
    def __init__(self, sample_file=None, normalization_mode=None,
                 load_from_file=None):
        assert (sample_file and normalization_mode) or load_from_file
        if sample_file:
            self.features_stats = stats_of_sample(sample_file)
            self.normalization_mode = normalization_mode
        else:
            self.normalization_mode, *stats = read_lines(load_from_file)
            self.features_stats = [
                dict(zip(('min', 'max', 'mean', 'std'),
                         (float(i) for i in s.split(' ')))) for s in stats]
        assert self.normalization_mode in {'min_max', 'z_score'}
        if self.normalization_mode == 'min_max':
            self.normalization_map = lambda v, i: min_max_norm(
                v, self.features_stats[i]['min'], self.features_stats[i]['max'])
        if self.normalization_mode == 'z_score':
            self.normalization_map = lambda v, i: z_score_norm(
                v, self.features_stats[i]['mean'], self.features_stats[i]['std'])

    def normalize(self, states):
        states_normalized = []
        for s in states:
            states_normalized.append(
                [self.normalization_map(s[i],i) for i in range(len(s))]
            )
        return states_normalized

    def save(self, path):
        write_line(self.normalization_mode, path)
        for s in self.features_stats:
            append_line(f"{s['min']} {s['max']} {s['mean']} {s['std']}", path)


