python3 reinforce.py \
	EXAMPLES/EASY \
	--step_limit 100 \
	--batch_size 100 \
	--inferences_per_step 100 \
	> `echo $0 | sed 's/\.sh/.log/g'`
