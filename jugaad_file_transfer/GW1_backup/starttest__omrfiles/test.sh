#!/bin/bash
hash=$1

echo "We are now calling Procmon on the profiler from the Gateway1" 
ssh jugaad@192.168.2.27 "python C:\\Profiler_OS_NW\\procmonallan.py '$hash' 120"

sshpass -p "jug@@d*%$" scp jugaad@192.168.2.27:c:/Profiler_OS_NW/OS_Data_csv/"$hash.csv" /home/jugaad/jugaad/temp_trail_storage/

echo "File transferred to Gateway1"
sshpass -p "jug@@d*%$" scp /home/jugaad/jugaad/temp_trail_storage/"$hash.csv" jugaad@202.141.30.50:/home/omr/reporthash/

echo "File transferred to Gateway2"

rm /home/jugaad/jugaad/temp_trail_storage/$hash.csv

echo "Remote profiler call executed successfully"
