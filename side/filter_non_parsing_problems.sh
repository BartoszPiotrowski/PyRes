PROBLEMS_DIR=$1
find $PROBLEMS_DIR -type f -name '*.p' | parallel --timeout 1 'python pyres-fof.py --silent {} > {.}.out 2> {.}.err'
find $PROBLEMS_DIR -name '*err' | xargs grep '.' -l | sed 's/\.err/.p/g'> _not_parsing
cat _not_parsing | xargs rm
rm $PROBLEMS_DIR/*err
rm $PROBLEMS_DIR/*out
rm _not_parsing
