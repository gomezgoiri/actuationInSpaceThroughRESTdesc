#! /bin/bash

export eulerjarpath="../../Euler.jar"

#java -jar $eulerjarpath --help
#java -jar $eulerjarpath --nope --quick-answer light_together.n3 --query light_goal.n3 # short answer
java -jar $eulerjarpath light_together.n3 --query light_goal.n3 # answer with proofs