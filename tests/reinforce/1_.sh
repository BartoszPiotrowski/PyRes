
python3 reinforce.py \
	BENCHMARKS/B3_100 \
	--units_in_hidden_layer 128 \
	--episodes 500 \
	--step_limit 10 \
	--batch_size 10 \
	--inferences_per_step 10 \
	--evaluate_each 3 \
	--policy_train_mode 'stochastic' \
	--policy_eval_mode 'stochastic' \
	--sample_states data/states_rand_B3.csv \
	--normalization_mode min_max

