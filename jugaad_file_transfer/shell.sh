#!/bin/bash

# Hardcoded destination information
DEST_USER="jugaad"        # Replace with the hardcoded destination username
DEST_IP="192.168.3.1"     # Replace with the hardcoded destination IP address
DEST_PASSWORD="jug@@d*%$" # Replace with the hardcoded password

# Hardcoded source directory (where the file is located)
SOURCE_DIR="/home/omr/files"  # e.g., "/home/user123/my_files"

# Specify the destination directory on the remote machine
DEST_DIR="/home/jugaad/jugaad/Malware/Profiler_OS_NW/omrmalwares"  # e.g., "/home/user123/Documents"

# Check if the correct number of arguments is provided (only 1 argument for file name)
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <file_name>"
    exit 1
fi

# Argument: file name
FILE_NAME=$1

# Full path to the file in the hardcoded source directory
SOURCE_FILE="$SOURCE_DIR/$FILE_NAME"

# Use scp to copy the file to the specified destination directory on the remote machine
# Using sshpass for password-based authentication
sshpass -p "$DEST_PASSWORD" scp "$SOURCE_FILE" "$DEST_USER@$DEST_IP:$DEST_DIR"

# Check if scp command was successful
if [ $? -eq 0 ]; then
    echo "File '$FILE_NAME' successfully copied from '$SOURCE_DIR' to '$DEST_USER@$DEST_IP:$DEST_DIR'."
else
    echo "Failed to copy the file."
fi

