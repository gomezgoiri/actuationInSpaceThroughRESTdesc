#! /bin/bash

source ../config.sh
#export folder=/tmp/tmp4uDskV/results/*

# Uniformize dataset_path to have an slash at the end
case "$1" in
*/)
    #echo "has slash"
    export folder="$1*"
    ;;
*)
    #echo "doesn't have a slash"
    export folder="$1/*"
    ;;
esac


for result_file in $folder
do
  echo "Printing results for file: $result_file"
  python $pyprojectpath/wot2013/evaluation/parser.py -i $result_file
done