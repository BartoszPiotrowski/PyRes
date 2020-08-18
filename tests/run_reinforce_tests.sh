for f in `find tests/reinforce/*`
do
	echo Running test $f
	./$f &> $f.log
	if [[ $? -eq 0 ]]
	then
		echo Test $f PASSED.
	else
		echo Test $f FAILED.
	fi
done
