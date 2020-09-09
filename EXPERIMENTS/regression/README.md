# Random forest fit

![](stats.csv_ALG198+1.p.png?raw=true)
![](stats.csv_KRS139+1.p.png?raw=true)
![](stats.csv_KRS165+1.p.png?raw=true)
![](stats.csv_KRS169+1.p.png?raw=true)
![](stats.csv_LCL414+1.p.png?raw=true)
![](stats.csv_LCL678+1.001.p.png?raw=true)
![](stats.csv_LCL684+1.001.p.png?raw=true)
![](stats.csv_LCL686+1.005.p.png?raw=true)
![](stats.csv_MGT013+1.p.png?raw=true)
![](stats.csv_MGT036+3.p.png?raw=true)
![](stats.csv_MSC012+1.p.png?raw=true)
![](stats.csv_NUM395+1.p.png?raw=true)
![](stats.csv_NUM489+3.p.png?raw=true)
![](stats.csv_NUM519+3.p.png?raw=true)
![](stats.csv_PHI014+1.p.png?raw=true)
![](stats.csv_SET589+3.p.png?raw=true)
![](stats.csv_SET592+3.p.png?raw=true)
![](stats.csv_SET625+3.p.png?raw=true)
![](stats.csv_SET915+1.p.png?raw=true)
![](stats.csv_SEU139+1.p.png?raw=true)
![](stats.csv_SEU161+3.p.png?raw=true)
![](stats.csv_SEU167+3.p.png?raw=true)
![](stats.csv_SEU275+1.p.png?raw=true)
![](stats.csv_SWB003+2.p.png?raw=true)
![](stats.csv_SWB007+2.p.png?raw=true)
![](stats.csv_SWV011+1.p.png?raw=true)
![](stats.csv_SYN054+1.p.png?raw=true)
![](stats.csv_SYN317+1.p.png?raw=true)
![](stats.csv_SYN336+1.p.png?raw=true)
![](stats.csv_SYN345+1.p.png?raw=true)
![](stats.csv_SYN355+1.p.png?raw=true)
![](stats.csv_SYN380+1.p.png?raw=true)
![](stats.csv_SYN389+1.p.png?raw=true)
![](stats.csv_SYN409+1.p.png?raw=true)
![](stats.csv_SYN724+1.p.png?raw=true)
![](stats.csv_SYN730+1.p.png?raw=true)
![](stats.csv_SYN733+1.p.png?raw=true)
![](stats.csv_SYN923+1.p.png?raw=true)
![](stats.csv_SYN931+1.p.png?raw=true)
![](stats.csv_SYN948+1.p.png?raw=true)
![](stats.csv_SYN950+1.p.png?raw=true)
![](stats.csv_SYN951+1.p.png?raw=true)
![](stats.csv_SYN967+1.p.png?raw=true)
![](stats.csv_SYN971+1.p.png?raw=true)
![](stats.csv_TOP021+1.p.png?raw=true)


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

#rm -rf EXPERIMENTS/regression/sstats*
find  EXPERIMENTS/regression/logs/ -type f | \
	EXPERIMENTS/regression/scripts/sstats.py EXPERIMENTS/regression/sstats.csv
./EXPERIMENTS/regression/scripts/sstats.R \
	EXPERIMENTS/regression/sstats.csv

```
