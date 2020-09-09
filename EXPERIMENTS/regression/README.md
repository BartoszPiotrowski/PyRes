# Random forest fit

![](stats.csv_KRS134+1.p.png?raw=true)
![](stats.csv_KRS141+1.p.png?raw=true)
![](stats.csv_LCL644+1.001.p.png?raw=true)
![](stats.csv_LCL650+1.001.p.png?raw=true)
![](stats.csv_MGT009+1.p.png?raw=true)
![](stats.csv_MGT016+1.p.png?raw=true)
![](stats.csv_NUM634+3.p.png?raw=true)
![](stats.csv_SET002+3.p.png?raw=true)
![](stats.csv_SET047+1.p.png?raw=true)
![](stats.csv_SET583+3.p.png?raw=true)
![](stats.csv_SEU152+1.p.png?raw=true)
![](stats.csv_SWB001+2.p.png?raw=true)
![](stats.csv_SWV011+1.p.png?raw=true)
![](stats.csv_SYN050+1.p.png?raw=true)
![](stats.csv_SYN341+1.p.png?raw=true)
![](stats.csv_SYN361+1.p.png?raw=true)
![](stats.csv_SYN364+1.p.png?raw=true)
![](stats.csv_SYN369+1.p.png?raw=true)
![](stats.csv_SYN377+1.p.png?raw=true)
![](stats.csv_SYN380+1.p.png?raw=true)
![](stats.csv_SYN381+1.p.png?raw=true)


# Reproducing the experiment

```
git checkout regression-1
export TPTP=/path/to/TPTP-v7.3.0

shuf BENCHMARKS/B3 > EXPERIMENTS/regression/all_probs
head -300 EXPERIMENTS/regression/all_probs > EXPERIMENTS/regression/train_probs
tail -86 EXPERIMENTS/regression/all_probs > EXPERIMENTS/regression/test_probs
rm -rf EXPERIMENTS/regression/logs
./EXPERIMENTS/regression/scripts/prep.py \
	EXPERIMENTS/regression/train_probs \
	EXPERIMENTS/regression/logs > \
	EXPERIMENTS/regression/to_run
./EXPERIMENTS/regression/scripts/run.sh EXPERIMENTS/regression/to_run

rm -rf EXPERIMENTS/regression/stats*
find  EXPERIMENTS/regression/logs/ -type f | \
	EXPERIMENTS/regression/scripts/stats.py EXPERIMENTS/regression/stats.csv
./EXPERIMENTS/regression/scripts/stats.R \
	EXPERIMENTS/regression/stats.csv

```
