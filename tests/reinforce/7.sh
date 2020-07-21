python3 reinforce.py \
	BENCHMARKS/B3_100 \
	--episodes 5000 \
	--learning_rate 0.001 \
	--step_limit 10 \
	--batch_size 10 \
	--inferences_per_step 10 \
	--evaluate_each 10 \
	--policy_train_mode 'semi-deterministic' \
	--policy_eval_mode 'semi-deterministic' \
	--sample_states data/states_rand_B3.csv \
	--normalization_mode min_max

