
Files in this folder
-------------------

This folder contains the following files:

 * create_experimental_environment.sh
      Creates the files needed to execute the different scenarios in a temporary folder
 * execute_benchmarks.sh [folder]
      Executes the different scenarios defined by the configuration files in the folder provided as a parameter
      It writes the ouput on several files under tmpfolder/results
 * process_results.sh [folder]
      To interpret the results of the executions of several scenarios
 * simulate_scenario.sh
      Given a configuration file for an scenario, it executes it
 * *.n3
      Main files of the reasoning process
 * *.tpl
      Template files used to generate the temporary files needed for the benchmarks
 * results/
      Folder with the results of a typical execution


Execution of the evaluation
---------------------------
To execute the evaluation, just call in this order to:

 1. bash create_experimental_environment.sh
 2. bash execute_benchmarks.sh [tmp_folder]
 3. bash process_results.sh [tmp_folder]


Python dependencies
-------------------

Make sure that you have the following dependencies installed for Python:
 - rdflib
 - networkx
 - numpy