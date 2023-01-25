#! /usr/bin/env bash
###############################################################################
# Script for "deploying" turboTurtle to /projects/aea_compute/aea-abaqus-python
#
# Usage: ./DEPLOY.sh
#
# NOTE: You must have a connection to the yellow network to successfully run
# this script
#
###############################################################################

#----------DEPLOY VARIABLES------------#
project_dir="turbo-turtle"
aea_compute_dir="/projects/aea_compute"
abq_python_dir="aea-abaqus-python"
deploy_directory="$aea_compute_dir/$abq_python_dir/$project_dir"
deploy_script=$(basename "$0")

declare -a files_list=$(ls -I ".*" -I $deploy_script)

# Make the deploy directory, if it does not already exist
mkdir -p $deploy_directory

# Copy files in the files_list to the deploy directory using rsync
for file_name in ${files_list[@]}; do
    rsync -r $file_name $deploy_directory/$file_name
done
