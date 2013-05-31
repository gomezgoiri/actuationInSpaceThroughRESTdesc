#!/bin/bash

export dataset_path=$1
export default_unrel_graphs=1
export default_unrel_rules=1
export default_unrelated=1


function get_config_file() {
  config_file=$dataset_path"scenario_$1_$2_$3.config"
}

function get_result_file() {
  result_file=$results_path"/r_$1_$2_$3.out"
}


#for i in {1..5}
#for i in {0..10..2}
#for i in 1 2 3 4 5
#echo "Welcome $i times"

echo "The path is $dataset_path"
results_path=$dataset_path"results"
mkdir $results_path
echo "Results path created in $results_path"

for unrel_graph in 1 100
do
  get_config_file $unrel_graph $default_unrel_rules $default_unrelated
  #echo $config_file
  get_result_file $unrel_graph $default_unrel_rules $default_unrelated
  echo $result_file
  `bash simulate_scenario.sh $config_file > $result_file 2>&1`
done 
