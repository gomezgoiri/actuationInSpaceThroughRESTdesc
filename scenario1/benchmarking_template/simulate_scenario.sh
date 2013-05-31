#! /bin/bash

export PYTHONPATH=$PYTHONPATH:../ScnImpl

#echo $1
python ../ScnImpl/wot2013/scenario.py -i $1 -e ../../