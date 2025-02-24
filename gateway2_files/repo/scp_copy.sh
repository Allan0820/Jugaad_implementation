#!/bin/bash

# Check if the right number of arguments are provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <filename_without_extension> <remote_user> <remote_host>"
    exit 1
fi

FILENAME_WITHOUT_EXTENSION=$1
REMOTE_USER=$2
REMOTE_HOST=$3

# Hardcoded path to the source directory
SOURCE_DIRECTORY="/home/jugaad/OS_DataFromProfiler"  # Replace with your actual source directory

# Construct the full source file path
SOURCE_FILE="$SOURCE_DIRECTORY/$FILENAME_WITHOUT_EXTENSION.csv"

# Remote destination directory (can also be hardcoded or passed as an argument)
REMOTE_DIRECTORY="/home/omr/report"  # Replace with your actual remote directory

# Use scp to copy the file to the remote machine
scp "$SOURCE_FILE" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_DIRECTORY"

# Check if the scp command was successful
if [ $? -eq 0 ]; then
    echo "File copied successfully to $REMOTE_USER@$REMOTE_HOST:$REMOTE_DIRECTORY"
else
    echo "Error occurred during file transfer."
fi

