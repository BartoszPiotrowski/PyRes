STATS_DIR=tests/reinforce/9
rm $STATS_DIR/*
python3 reinforce.py \
	BENCHMARKS/B3_10 \
	--episodes 5000 \
	--step_limit 100 \
	--batch_size 5 \
	--inferences_per_step 10 \
	--evaluate_each 10 \
	--policy_train_mode 'stochastic' \
	--policy_eval_mode 'stochastic' \
	--sample_states data/states_rand_B3.csv \
	--normalization_mode min_max \
	--stats_dir $STATS_DIR
./side/visualize.sh $STATS_DIR
viewnior $STATS_DIR/*png

