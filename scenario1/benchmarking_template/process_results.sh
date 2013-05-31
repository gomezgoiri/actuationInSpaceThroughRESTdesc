#! /bin/bash

export PYTHONPATH=$PYTHONPATH:../ScnImpl

#export folder=/tmp/tmp4uDskV/results/*
export folder="$1/*"


for result_file in $folder
do
  echo "Printing results for file: $result_file"
  python ../ScnImpl/wot2013/evaluation/parser.py -i $result_file
done