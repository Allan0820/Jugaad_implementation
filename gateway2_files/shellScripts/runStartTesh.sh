#!/bin/bash

# Arguments passed from the Python function
REMOTE_HOST=$1
REMOTE_USER=$2
REMOTE_DIRECTORY=$3
REMOTE_PYTHON_SCRIPT=$4
PYTHON_ARG=$5

echo "Inside the shell script"
echo "The arguments passed to the runstarttest script are as follows"
echo "$@"


# SSH into the remote machine and run the Python script with the argument
ssh ${REMOTE_USER}@${REMOTE_HOST} "cd ${REMOTE_DIRECTORY} && python3 ${REMOTE_PYTHON_SCRIPT} ${PYTHON_ARG}"
