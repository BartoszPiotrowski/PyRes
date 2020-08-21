STATS_DIR=tests/reinforce/10
rm $STATS_DIR/*
python3 reinforce.py \
	'BENCHMARKS/B_NUM519+1' \
	--episodes 5000 \
	--step_limit 100 \
	--batch_size 1 \
	--inferences_per_step 100 \
	--evaluate_each 10 \
	--policy_train_mode 'stochastic' \
	--policy_eval_mode 'stochastic' \
	--sample_states data/states_rand_B3.csv \
	--normalization_mode min_max \
	--stats_dir $STATS_DIR

