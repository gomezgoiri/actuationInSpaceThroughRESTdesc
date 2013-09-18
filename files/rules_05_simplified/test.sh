#! /bin/bash

source ../config.sh

#java -jar $eulerjar facts.n3 light3_rule.n3 --query light_goal.n3
java -jar $eulerjar new_facts.n3 light3_rule.n3 --query light_goal.n3