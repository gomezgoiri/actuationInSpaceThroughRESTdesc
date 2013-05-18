#! /bin/bash

#java -jar ../../Euler.jar light_together.n3 --query light_goal.n3 # more difficult to interpret
java -jar ../../Euler.jar new_facts.n3 light1_rule.n3 light2_rule.n3 light3_rule.n3 temperature_rule.n3 unrelated_rule.n3 preference_fact.n3 --query light_goal.n3