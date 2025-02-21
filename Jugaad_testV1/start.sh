#!/bin/bash 

cd ${PWD}

python3 app.py
echo "started application server" 
python3 email_function.py
echo "started email script"


