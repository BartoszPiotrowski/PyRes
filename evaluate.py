import os
import numpy as np
from tempfile import mkdtemp
from glob import glob
from utils import read_lines


def evaluate(problems_list, pyres_options, timeout, policy_model,
             policy_eval_mode):
    proof_dir = mkdtemp()
    os.popen('./evaluate.sh ' + \
    ' '.join([problems_list, policy_model, policy_eval_mode, str(timeout),
              proof_dir, pyres_options])).read()
    outputs = glob(proof_dir + '/*')
    stats_from_output(outputs)
    # TODO remove proof_dir


def evaluate_random(problems_list, pyres_options, timeout, probabilities):
    proof_dir = mkdtemp()
    probabilities = ','.join([str(p) for p in probabilities])
    os.popen('./evaluate_random.sh ' + \
    ' '.join([problems_list, probabilities, str(timeout), proof_dir,
              pyres_options])).read()
    outputs = glob(proof_dir + '/*')
    stats_from_output(outputs)


def stats_from_output(outputs):
    success, time, processed = [], [], []
    for o in outputs:
        lines = read_lines(o)
        if 'SZS status Theorem' in ' '.join(lines):
            success.append(1)
            for l in lines:
                if 'User time' in l:
                    time.append(float(l.split(' ')[-2]))
                if 'Processed clauses' in l:
                    processed.append(int(l.split(' ')[-1]))
        else:
            success.append(0)
    assert len(time) == len(processed)
    assert len(outputs) == len(success)

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

