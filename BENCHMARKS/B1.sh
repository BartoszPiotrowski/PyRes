# $TPTP -- path to TPTP
find $TPTP -name '*+*.p' |
	xargs grep 'Rating   : 0.0[01]' -l |
	xargs realpath --relative-to=$TPTP > problems_not_filtered_by_pyres
for p in `cat problems_not_filtered_by_pyres`
do
	echo $p
	timeout 1 ./pyres-fof.py --silent $p 2> aaa
	[ -s aaa ] || echo $p >> problems_filtered_by_pyres
done
cp problems_filtered_by_pyres BENCHMARKS/B1
rm problems_*_pyres
shuf BENCHMARKS/B1 | head -100 > BENCHMARKS/B1_100
shuf BENCHMARKS/B1 | head -10 > BENCHMARKS/B1_10

