#! /bin/bash

# Configure the following paths
export pyprojectpath="../ScnImpl"
export eulerjarpath="../"


# Don't touch this >>>
# because these variables will be used by the scripts in the subfolders!
export pyprojectpath="../"$pyprojectpath
export eulerjarpath="../"$eulerjarpath
export eulerjar=$eulerjarpath"Euler.jar"
export PYTHONPATH=$PYTHONPATH:$pyprojectpath
# <<< Don't touch this