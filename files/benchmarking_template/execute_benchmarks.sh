#!/bin/bash


export dataset_path=$1
export default_unrel_graphs=1
export default_unrel_rules=1
export default_not_feasible_rules=1


# Uniformize dataset_path to have an slash at the end
case "$dataset_path" in
*/)
    #echo "has slash"
    ;;
*)
    #echo "doesn't have a slash"
    export dataset_path="$dataset_path/"
    ;;
esac





function get_config_file() {
  config_file=$dataset_path"scenario_$1_$2_$3.config"
}

function get_result_file() {
  result_file=$results_path"r_$1_$2_$3.out"
}


#for i in {1..5}
#for i in {0..10..2}
#for i in 1 2 3 4 5
#echo "Welcome $i times"

echo "The path is $dataset_path"
results_path=$dataset_path"results"
mkdir $results_path
echo "Results path created in $results_path"



for config_file in $dataset_path*.config # since I am not talking about a string but about a file/folder, without ""
do
  #echo $confile
  filename=$(basename "$config_file")
  #extension="${filename##*.}"
  filename="${filename%.*}"
  #echo $filename
  result_file=$results_path"/$filename.out"
  echo "Processing $config_file > $result_file"
  `bash simulate_scenario.sh $config_file > $result_file 2>&1`
done


#for unrel_graph in 1 100
#do
#  get_config_file $unrel_graph $default_unrel_rules $default_not_feasible_rules
#  echo $config_file
#  get_result_file $unrel_graph $default_unrel_rules $default_not_feasible_rules
#  echo $result_file
#  `bash simulate_scenario.sh $config_file > $result_file 2>&1`
#done