#!/bin/bash 
cd Uploaded_files
echo ON
while [[ 1 -gt 0 ]]
do

for file in  `ls | grep ".zip"`;do
  sha512sum "${file}" | cut -d " " -f 1 > ${file}_hash.txt
  zip "[AC]${file}" $file ${file}_hash.txt
  rm ${file}
  rm ${file}_hash.txt
  scp /home/allan/Desktop/OMR_CB/Jugaad_test/instance/Uploaded_files/"[AC]${file}" jugaadvmvb@192.168.43.65:/home/jugaadvmvb/supply_of_samples
 
  rm [AC]${file}
#  mv "[AC]${file}" /home/allan/Desktop/filestorejugaad 
  clear
  echo ON
done
done
echo OFF
