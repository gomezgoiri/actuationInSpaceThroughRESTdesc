#! /bin/bash

export INPUT_RESULT_FILE=../rules_03/result.txt
export TEMPORARY_FILE=./tmp_unblank.n3

python unblank_lemmas.py -i $INPUT_RESULT_FILE -o $TEMPORARY_FILE

java -jar ../../Euler.jar --nope $TEMPORARY_FILE --query lemmas.n3 > lemmas.txt

java -jar ../../Euler.jar --nope $TEMPORARY_FILE --query lemma_precedences.n3 > precedences.txt

java -jar ../../Euler.jar --nope $TEMPORARY_FILE --query rest_bindings.n3 > bindings.txt

java -jar ../../Euler.jar --nope $TEMPORARY_FILE --query rest_services.n3 > services.txt

rm tmp_unblank.n3