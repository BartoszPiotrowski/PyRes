PROBLEMS=$1
POLICY_MODEL=$2
POLICY_EVAL_MODE=$3
TIMEOUT=$4
PROOF_DIR=$5
PYRES_OPTS=$6

cat $PROBLEMS | \
	parallel --timeout $TIMEOUT \
	"python3 pyres-fof.py $PYRES_OPTS --silent --policy-model $POLICY_MODEL --policy-eval-mode $POLICY_EVAL_MODE {} > $PROOF_DIR/{/.}.out" \
	2> _evaluate.err
# TODO print errors
