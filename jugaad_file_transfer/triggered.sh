#!/bin/bash

# Check if correct arguments are provided
if [ $# -ne 5 ]; then
    echo "Usage: $0 <username> <password> <ip_address> <directory_path> <python_argument>"
    exit 1
fi

# Assign command-line arguments to variables
USERNAME=$1
PASSWORD=$2
IP_ADDRESS=$3
REMOTE_DIR=$4
PYTHON_ARG=$5

# SSH into the remote machine and execute the Python script with the argument
sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no "$USERNAME@$IP_ADDRESS" << EOF
    cd "$REMOTE_DIR"
    python3 startModifiedTest.py "$PYTHON_ARG"
EOF

