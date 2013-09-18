#! /bin/bash

source ../config.sh

export OUTPUT_DIR=/tmp
workon wot2013

python $pyprojectpath/wot2013/proofs/extract_info.py -i result_gt16.txt -o $OUTPUT_DIR -e ../../
python $pyprojectpath/wot2013/proofs/interpretation/graphs.py -i $OUTPUT_DIR/precedences.txt # filtered deleting repeated REST calls
#python $pyprojectpath/wot2013/proofs/interpretation/rest_parser.py -i $OUTPUT_DIR/services.txt -f /tmp -b $OUTPUT_DIR/bindings.txt > rest.txt