#! /bin/env python3
import os, sys
out_dir = sys.argv[1]
problems_file = 'BENCHMARKS/B3'
basic_params = '-tifb -nlargest -HPickGivenRandom'
out_dir_basic_params = os.path.join(out_dir, basic_params.replace(' ', ''))
age_queue_probabilities = [x / 1000 for x in range(1001)]
with open(problems_file, 'r') as f:
    problems_list = f.read().splitlines()
for p in age_queue_probabilities:
    p_dir = os.path.join(out_dir_basic_params, str(p))
    os.makedirs(p_dir)
    for P in problems_list:
        print(
            f"./pyres-fof.py {basic_params} -a{p} {P} "
            f"> {os.path.join(p_dir, os.path.basename(P))}"
        )

