#! /bin/env python3
import os, sys
train_probs = sys.argv[1]
out_dir = sys.argv[2]
basic_params = '-tifbs -nlargest -HPickGivenRandom'
out_dir_basic_params = os.path.join(out_dir, basic_params.replace(' ', ''))
age_queue_probabilities = [x / 1000 for x in range(1001)]
with open(train_probs, 'r') as f:
    problems_list = f.read().splitlines()
for p in age_queue_probabilities:
    p_dir = os.path.join(out_dir_basic_params, str(p))
    os.makedirs(p_dir)
    for P in problems_list:
        print(
            f"./pyres-fof.py {basic_params} -a{p} {P} "
            f"> {os.path.join(p_dir, os.path.basename(P))}"
        )

