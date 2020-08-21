# TODO
- recording stats and visualizing
- clipping of the inf loss
- decrease the temperature with time
- avoid running out of memory
- define new queues / heuristics
	- similarity to conjecture
- extract more proof state features
- investigate why some problems from ALG cannot be parsed in a finite time
- deterministic action selection?
- negative reward?
- larger reward for harder proofs?
- normalizing the reward? (see Pong from pixels)

# DONE
- implement policy network
- implement the reinforce algorithm
- implement heuristic using the policy network
- integrate the reinforce algorithm with the saturation algorithm
- parallel processing -- multiple problems (= episodes) run at once

# IDEAS
- normalization of the proof state vector
- reward based on whether the chosen queue picked a clause which ended up in
  the proof
