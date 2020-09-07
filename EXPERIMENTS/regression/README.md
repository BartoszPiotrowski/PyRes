# Reproducing the experiment
```
git checkout regression-1

shuf BENCHMARKS/B3 > EXPERIMENTS/regression/all_probs
head -300 EXPERIMENTS/regression/all_probs > EXPERIMENTS/regression/train_probs
tail -86 EXPERIMENTS/regression/all_probs > EXPERIMENTS/regression/test_probs
rm -rf EXPERIMENTS/regression/logs
./EXPERIMENTS/regression/scripts/prep.py \
	EXPERIMENTS/regression/train_probs \
	EXPERIMENTS/regression/logs > \
	EXPERIMENTS/regression/to_run
./EXPERIMENTS/regression/scripts/run.sh EXPERIMENTS/regression/to_run

rm -rf EXPERIMENTS/regression/stats
mkdir EXPERIMENTS/regression/stats
find  EXPERIMENTS/regression/logs/ -type f | \
	EXPERIMENTS/regression/scripts/stats.py EXPERIMENTS/regression/stats

find EXPERIMENTS/regression/stats/ -name '*.p' | \
	grep 'yes' -l | xargs grep 'no' -l | xargs -l1 \
	./EXPERIMENTS/regression/scripts/stats.R
```