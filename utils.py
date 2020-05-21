import os
import pickle
import gzip


def read_lines(filename):
    with open(filename, encoding ='utf-8') as f:
        return f.read().splitlines()


def write_lines(list_of_lines, filename):
    with open(filename, encoding ='utf-8', mode='wt') as f:
        f.write('\n'.join(list_of_lines) + '\n')


def append_lines(list_of_lines, filename):
    with open(filename, encoding ='utf-8', mode='a') as f:
        f.write('\n'.join(list_of_lines) + '\n')

def save_obj(obj, filename):
    with gzip.open(filename, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(filename):
    with gzip.open(filename, 'rb') as f:
        return pickle.load(f)

