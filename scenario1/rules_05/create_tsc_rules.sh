#! /bin/bash

export PYTHONPATH=$PYTHONPATH:../ScnImpl

python ../ScnImpl/wot2013/clues/tsc_rules.py -i ./silly_example/facts.n3 -o silly_example/new_facts.n3