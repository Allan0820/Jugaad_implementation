#!/bin/bash 
count=0
while [[ 1 -gt 0 ]];do
for file in  `ls Uploaded_files/`;do 
  
  echo $file  $((count++))
done
done

