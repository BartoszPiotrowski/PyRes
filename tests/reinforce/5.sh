python3 reinforce.py \
	BENCHMARKS/B3_100 \
	--step_limit 10 \
	--batch_size 10 \
	--inferences_per_step 10 \
	--evaluate_each 3 \
	--temperature 1.5 \
	--sample_states data/states_rand_B3.csv \
	--normalization_mode min_max
