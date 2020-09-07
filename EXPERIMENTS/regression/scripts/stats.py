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
        if '# Initial clauses' in Ol:
            init_c = Ol.split(': ')[1]
        if '# Initial mean length' in Ol:
            init_l = Ol.split(': ')[1]
        if '# Initial mean weight' in Ol:
            init_w = Ol.split(': ')[1]
        if '# Processed' in Ol:
            proc = Ol.split(': ')[1]
    prov = 'yes' if not proc == str(0) else 'no'
    to_append = f"{P},{p},{prov},{init_c},{init_l},{init_w},{proc}\n"
    with open(sys.argv[1], 'a') as f:
        f.write(to_append)


