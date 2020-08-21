#!/bin/sh

find $1 -name '*.out' | xargs -l1 side/visualize.R

