rm data/states_rand_B2.csv
python3 randomly.py \
	BENCHMARKS/B3 \
	--step_limit 100 \
	--batch_size 20 \
	--inferences_per_step 100 \
	--save_states data/states_rand_B3.csv
