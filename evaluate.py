import os
import numpy as np


def evaluate(problems_dir, pyres_options, timeout, policy_model):
    output = os.popen('./evaluate.sh ' + \
     ' '.join([problems_dir, policy_model, str(timeout), pyres_options])).read()
    stats_from_output(output)

def stats_from_output(output):
    lines = output.split('\n')
    success, time, processed = [], [], []
    for l in lines:
        if 'SZS status' in l:
            if 'SZS status Theorem' in l:
                success.append(1)
            else: success.append(0)
        if 'User time' in l:
            time.append(float(l.split(' ')[-2]))
        if 'Processed clauses' in l:
            processed.append(int(l.split(' ')[-1]))
    assert len(success) == len(time) == len(processed)

    print(f'Successful runs                     : {sum(success):}')
    print(f'Average user time                   : {np.mean(time):.2f}')
    print(f'Average number of processed clauses : {np.mean(processed):.0f}')




if __name__=='__main__':
    # test
    evaluate('EXAMPLES/ALG', '"-tfb -nsmallest"', '10', 'tmp/policy_model.pt')
    # '" ... "' in the sencond argument is important if the options are
    # separated by whitespaces -- otherwise only the first thing will be passed

