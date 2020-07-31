mkdir -p $2
find $1 -type f | stats.py $2
