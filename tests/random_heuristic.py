#!/bin/python3

import sys
sys.path.append('.')
from evaluate import evaluate_random

granularity = 20
probabilities = [(p/granularity, 1-p/granularity) for p in range(granularity)]

for p in probabilities:
    print(f'Queue probabilities: {p}')
    evaluate_random('BENCHMARKS/B3_100', '-tifbp -nlargest', 10, p)
    print()
