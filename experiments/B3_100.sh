python3 reinforce.py \
	BENCHMARKS/B3_100 \
	--step_limit 100 \
	--batch_size 100 \
	--inferences_per_step 100 \
	| tee `echo $0 | sed 's/\.sh/.log/g'`