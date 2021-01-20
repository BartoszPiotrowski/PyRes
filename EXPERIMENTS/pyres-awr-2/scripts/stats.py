#! /bin/env python3

import sys

for l in sys.stdin:
    try:
        l = l.rstrip()
        P = l.split('/')[-1]
        p = l.split('/')[-2]
        proc = str(0)
        reso = str(0)
        init = str(0)
        proof_length = 0
        with open(l, 'r') as f:
            O = f.read().splitlines()
        for Ol in O:
            if Ol and not Ol[0] == '#':
                proof_length += 1
            if '# Processed clauses' in Ol:
                proc = Ol.split(': ')[1]
            if '# Resolvents computed' in Ol:
                reso = Ol.split(': ')[1]
            if '# Initial clauses' in Ol:
                init = Ol.split(': ')[1]
            if 'ResourceOut' in Ol and proof_length > 0:
                raise ValueError
        prov = 'yes' if not proc == str(0) else 'no'
        to_append = f"{p},{prov},{proc},{reso},{init},{str(proof_length)}\n"
        with open(sys.argv[1] + '/' + P, 'a') as f:
            f.write(to_append)
    except:
        pass
