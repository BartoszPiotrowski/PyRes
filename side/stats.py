#! /bin/env python3

import sys

for l in sys.stdin:
    l = l.rstrip()
    P = l.split('/')[-1]
    p = l.split('/')[-2]
    with open(l, 'r') as f:
        O = f.read().splitlines()
    proc = str(0)
    reso = str(0)
    init = str(0)
    for Ol in O:
        if '# Processed clauses' in Ol:
            proc = Ol.split(': ')[1]
        if '# Resolvents computed' in Ol:
            reso = Ol.split(': ')[1]
        if '# Initial clauses' in Ol:
            init = Ol.split(': ')[1]
    prov = 'yes' if not proc == str(0) else 'no'
    to_append = f"{p},{prov},{proc},{reso},{init}\n"
    with open(sys.argv[1] + '/' + P, 'a') as f:
        f.write(to_append)


