#! /bin/bash

java -jar ../../../Euler.jar facts.n3 light3_rule.n3 --query light_goal.n3
java -jar ../../../Euler.jar new_facts.n3 light3_rule.n3 --query light_goal.n3