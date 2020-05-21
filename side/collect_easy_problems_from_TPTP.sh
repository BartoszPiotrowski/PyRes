TPTP_DIR=$1
EASY_DIR=$2
ALL_PROBLEMS=`find $TPTP_DIR/Problems -type f -name '*+*.p'`
for f in $ALL_PROBLEMS
do
	grep 'Rating   : 0.0[01]' -v '-1' $f -l >> _easy
done

mkdir -p $EASY_DIR
cat _easy | xargs cp -t $EASY_DIR
rm _easy
cp -r $TPTP_DIR/Axioms $EASY_DIR
