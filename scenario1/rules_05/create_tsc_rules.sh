#! /bin/bash

export PYTHONPATH=$PYTHONPATH:../ScnImpl

python ../ScnImpl/wot2013/clues/tsc_rules.py -i ./facts.n3 -o new_facts.n3