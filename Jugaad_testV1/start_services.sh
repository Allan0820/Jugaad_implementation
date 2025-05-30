#!/bin/bash 
#run this script with sudo permissions only!!
source ./bin/activate &
sudo systemctl start app_duty.service &
sudo systemctl start email_duty.service &

echo "Application Server has started its duty!" &

 
