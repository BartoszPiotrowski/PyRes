import os
import numpy as np
from tempfile import mkdtemp
from glob import glob
from utils import read_lines, append_line, mkdir_if_not_exists


def evaluate(problems_list, pyres_options, timeout, policy_model,
             policy_eval_mode, stats_dir):
    proof_dir = mkdtemp()
    command = './evaluate.sh ' + ' '.join(
        [problems_list, policy_model, policy_eval_mode,
         str(timeout), proof_dir, pyres_options])
    os.popen(command).read()
    outputs = glob(proof_dir + '/*')
    stats_from_output(outputs, stats_dir)
    # TODO remove proof_dir


def evaluate_random(problems_list, pyres_options, timeout, probabilities):
    proof_dir = mkdtemp()
    probabilities = ','.join([str(p) for p in probabilities])
    os.popen('./evaluate_random.sh ' + \
    ' '.join([problems_list, probabilities, str(timeout), proof_dir,
              pyres_options])).read()
    outputs = glob(proof_dir + '/*')
    stats_from_output(outputs)


def stats_from_output(outputs, stats_dir=None):
    success, time, processed, age_weight = [], [], [], []
    for o in outputs:
        lines = read_lines(o)
        if 'SZS status Theorem' in ' '.join(lines):
            success.append(1)
            t, p, aw = 0, 0, 0
            for l in lines:
                if 'User time' in l:
                    t = float(l.split(' ')[-2])
                    time.append(t)
                if 'Processed clauses' in l:
                    p = int(l.split(' ')[-1])
                    processed.append(p)
                if 'Age / weight ratio' in l:
                    aw = float(l.split(' ')[-1])
                    age_weight.append(aw)
            if stats_dir:
                mkdir_if_not_exists(stats_dir)
                file = os.path.join(stats_dir, os.path.basename(o))
                to_append = f"{t},{p},{aw}"
                append_line(to_append, file)
        else:
            success.append(0)


    print(f'Problems solved                     : {sum(success)} / {len(success)}')
    print(f'Average user time                   : {np.mean(time):.2f}')
    print(f'Average number of processed clauses : {np.mean(processed):.0f}')


if __name__=='__main__':
    # test
    print('Stochastic mode...')
    evaluate('BENCHMARKS/B3_100', '"-tfb -nsmallest"', '10', 'policy_model.pt',
             'stochastic')
    print('Deterministic mode...')
    evaluate('BENCHMARKS/B3_100', '"-tfb -nsmallest"', '10', 'policy_model.pt',
             'deterministic')
    # '" ... "' in the sencond argument is important if the options are
    # separated by whitespaces -- otherwise only the first thing will be passed

