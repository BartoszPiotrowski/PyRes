PROBLEMS=$1
PROBS=$2
TIMEOUT=$3
PROOF_DIR=$4
PYRES_OPTS=$5

cat $PROBLEMS | \
	parallel --timeout $TIMEOUT \
	"python3 pyres-fof.py $PYRES_OPTS --silent --random-heuristic $PROBS {} > $PROOF_DIR/{/.}.out" \
	2> evaluate_random.err
