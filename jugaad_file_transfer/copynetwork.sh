#!/bin/bash

# Check if the correct number of arguments is provided
if [ $# -ne 2 ]; then
  echo "Usage: $0 <source_folder_name> <destination_folder_name>"
  exit 1
fi

# Assign arguments to variables
SOURCE_DIR="/home/jugaad/NetworkData/GW1/eno1/M$1"

DEST_DIR="/home/omr/report/$2"

# Check if the source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
  echo "Source directory $SOURCE_DIR does not exist."
  exit 1
fi

# Check if the destination directory exists
if [ ! -d "$DEST_DIR" ]; then
  echo "Destination directory $DEST_DIR does not exist."
  exit 1
fi

# Copy all files from the source to the destination directory
cp -r "$SOURCE_DIR"/* "$DEST_DIR/"

# Confirm completion
echo "Files from $SOURCE_DIR copied to $DEST_DIR successfully."

