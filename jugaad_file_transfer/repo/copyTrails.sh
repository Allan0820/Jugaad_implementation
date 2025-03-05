#!/bin/bash

# Check if the right number of arguments are provided
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <source_file_path> <remote_user> <remote_host> <remote_directory>"
    exit 1
fi

SOURCE_FILE=$1
REMOTE_USER=$2
REMOTE_HOST=$3
REMOTE_DIRECTORY=$4

# Use scp to copy the file to the remote machine
scp "$SOURCE_FILE" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_DIRECTORY"

# Check if the scp command was successful
if [ $? -eq 0 ]; then
    echo "File copied successfully to $REMOTE_USER@$REMOTE_HOST:$REMOTE_DIRECTORY"
else
    echo "Error occurred during file transfer."
fi






















