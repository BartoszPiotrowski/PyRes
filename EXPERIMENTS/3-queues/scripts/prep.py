#! /bin/env python3
import os, sys
problems_file = sys.argv[1]
out_dir = sys.argv[2]
basic_params = '-tifbp -nlargest -HThreeQueuesRandom'
out_dir_basic_params = os.path.join(out_dir, basic_params.replace(' ', ''))
dist_queue_probabilities = [x / 100 for x in range(101)]
age_queue_probabilities    = [(1/6) * (1 - x) for x in dist_queue_probabilities]
weight_queue_probabilities = [(5/6) * (1 - x) for x in dist_queue_probabilities]
wad_probabilities_zip = zip(
    [str(x) for x in weight_queue_probabilities],
    [str(x) for x in age_queue_probabilities],
    [str(x) for x in dist_queue_probabilities])
wad_probabilities = [','.join(wad) for wad in wad_probabilities_zip]
with open(problems_file, 'r') as f:
    problems_list = f.read().splitlines()
for wad in wad_probabilities:
    wad_dir = os.path.join(out_dir_basic_params, wad)
    os.makedirs(wad_dir)
    for P in problems_list:
        print(
            f"./pyres-fof.py {basic_params} -q{wad} {P} "
            f"> {os.path.join(wad_dir, os.path.basename(P))}"
        )

