PROBLEMS=$1
POLICY_MODEL=$2
TIMEOUT=$3
PYRES_OPTS=$4

cat $PROBLEMS | \
	parallel --timeout $TIMEOUT \
	"python3 pyres-fof.py $PYRES_OPTS --silent --policy-model $POLICY_MODEL {}" \
	2> evaluate.err
