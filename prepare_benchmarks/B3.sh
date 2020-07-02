#!/bin/bash
mkdir BENCHMARKS/pyres-fof-proofs
cat BENCHMARKS/B2 |
	parallel --timeout 10 \
	"./pyres-fof.py -tifbp -HPickGiven5 -nlargest {} > BENCHMARKS/pyres-fof-proofs/{/.}.out" \
grep 'SZS status Theorem' BENCHMARKS/pyres-fof-proofs/* -l | \
	xargs -l1 basename | sed 's/.out/.p/g' | xargs -l1 find $TPTP -name | \
	xargs realpath --relative-to=$TPTP > BENCHMARKS/B3

mv BENCHMARKS/pyres-fof-proofs tmp

shuf BENCHMARKS/B3 | head -100 > BENCHMARKS/B3_100
shuf BENCHMARKS/B3 | head -10 > BENCHMARKS/B3_10

