#!/bin/bash
cat BENCHMARKS/B1 | parallel "grep 'include' -l $TPTP/{}" | \
	xargs realpath --relative-to=$TPTP > bad
comm -23 <(sort BENCHMARKS/B1) <(sort bad) > BENCHMARKS/B2
shuf BENCHMARKS/B2 | head -100 > BENCHMARKS/B2_100
shuf BENCHMARKS/B2 | head -10 > BENCHMARKS/B2_10

