#!/bin/bash

# Variables (Hardcoded)
REMOTE_USER="omr"
REMOTE_IP="202.141.30.50"  # Remote machine IP address
REMOTE_DIR="/home/omr/report/"  # Base directory on the remote machine where directories will be created
REMOTE_PASS="omr@jug@@d*%$"  # Password for the remote machine

# Input argument (filename)
FILE_NAME="$1"

# Check if the file exists
if [ ! -f "$FILE_NAME" ]; then
  echo "File $FILE_NAME does not exist."
  exit 1
fi

# Extract the base name of the file (to be used for the directory name)
DIR_NAME=$(basename "$FILE_NAME")

# Create the directory on the remote machine and set full permissions for all users and groups
sshpass -p "$REMOTE_PASS" ssh $REMOTE_USER@$REMOTE_IP "mkdir -p $REMOTE_DIR/$DIR_NAME && chmod 777 $REMOTE_DIR/$DIR_NAME"

# Check if the directory creation was successful
if [ $? -ne 0 ]; then
  echo "Failed to create directory $DIR_NAME on the remote machine."
  exit 1
fi

# Use scp with sshpass to copy the file into the newly created directory on the remote machine
sshpass -p "$REMOTE_PASS" scp "$FILE_NAME" "$REMOTE_USER@$REMOTE_IP:$REMOTE_DIR/$DIR_NAME/"

# Check if the file was successfully copied
if [ $? -eq 0 ]; then
  echo "File $FILE_NAME successfully copied to $REMOTE_IP:$REMOTE_DIR/$DIR_NAME/"
else
  echo "Failed to copy file $FILE_NAME."
  exit 1
fi
