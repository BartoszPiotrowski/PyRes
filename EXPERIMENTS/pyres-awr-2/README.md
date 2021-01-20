
# `pyres-awr-2`
This experiment is the same as `pyres-awr` but here
we also investigate and visualize the lengths of the proofs

# Selection of different plots

## Steady grow

![](stats/PUZ031+2.p.png?raw=true)
![](stats/SET599+3.p.png?raw=true)
![](stats/SYN070+1.p.png?raw=true)
![](stats/SYN072+1.p.png?raw=true)
![](stats/SYN375+1.p.png?raw=true)
![](stats/SYO578+1.p.png?raw=true)
![](stats/SEU139+1.p.png?raw=true)
![](stats/SWB029+2.p.png?raw=true)

## Proved for rare age queue only

![](stats/ALG171+1.p.png?raw=true)
![](stats/ALG174+1.p.png?raw=true)
![](stats/NLP117+1.p.png?raw=true)
![](stats/SYO580+1.p.png?raw=true)

## Proved for frequent age queue only

![](stats/NUM456+6.p.png?raw=true)
![](stats/SEU047+1.p.png?raw=true)

## Unimodal

![](stats/COM003+2.p.png?raw=true)
![](stats/NUM520+1.p.png?raw=true)
![](stats/RNG124+4.p.png?raw=true)
![](stats/RNG125+4.p.png?raw=true)
![](stats/SET910+1.p.png?raw=true)
![](stats/SEU139+2.p.png?raw=true)

## Bimodal

![](stats/COM013+4.p.png?raw=true)
![](stats/SEU123+2.p.png?raw=true)
![](stats/SEU294+1.p.png?raw=true)

## Success in small interval only

![](stats/SEU130+2.p.png?raw=true)
![](stats/NLP046+1.p.png?raw=true)

## Multiple *branches* or *clusters*

![](stats/KRS172+1.p.png?raw=true)
![](stats/KRS175+1.p.png?raw=true)
![](stats/MGT028+1.p.png?raw=true)
![](stats/SET589+3.p.png?raw=true)
![](stats/LCL686+1.005.p.png?raw=true)
![](stats/MGT014+1.p.png?raw=true)
![](stats/NUM395+1.p.png?raw=true)
![](stats/SET592+3.p.png?raw=true)
![](stats/SET626+3.p.png?raw=true)
![](stats/SEU295+3.p.png?raw=true)

## Strange

![](stats/SET907+1.p.png?raw=true)
![](stats/SEU306+1.p.png?raw=true)

# Reproducing the experiment
```
grep 'stats.*true' EXPERIMENTS/pyres-awr-2/README.md | cut -d/ -f2 | cut -d'?' -f1 | sed 's/.png//' > tmp/a
for l in `cat tmp/a`; do grep $l BENCHMARKS/B1; done > tmp/b
./EXPERIMENTS/pyres-awr-2/scripts/prep.py EXPERIMENTS/pyres-awr-2/logs > \
	EXPERIMENTS/pyres-awr-2/to_run
./EXPERIMENTS/pyres-awr-2/scripts/run.sh EXPERIMENTS/pyres-awr-2/to_run
mkdir EXPERIMENTS/pyres-awr-2/stats
find  EXPERIMENTS/pyres-awr-2/logs/ -type f | \
	./EXPERIMENTS/pyres-awr-2/scripts/stats.py EXPERIMENTS/pyres-awr-2/stats
find EXPERIMENTS/pyres-awr-2/stats/ -name '*.p' | xargs -l1 \
	./EXPERIMENTS/pyres-awr-2/scripts/stats.R
```
