#! /bin/bash

java -jar ../../Euler.jar ../rules_03/result.txt --query lemmas.n3 > lemmas.txt

java -jar ../../Euler.jar --nope ../rules_03/result.txt --query lemma_precedences.n3 > precedences.txt

java -jar ../../Euler.jar --nope ../rules_03/result.txt --query rest_bindings.n3 > bindings.txt

java -jar ../../Euler.jar --nope ../rules_03/result.txt --query rest_services.n3 > services.txt