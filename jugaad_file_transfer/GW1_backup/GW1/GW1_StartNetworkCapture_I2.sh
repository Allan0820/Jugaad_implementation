# To Call from remot
# GW1_StartNetworkCapture.sh <malware_id>  <Run_id> <interval_of_running_in_seconds>
# Eg. ~/jugaad/Malware/GW1/GW1_StartNetworkCapture.sh 1 1 180


tshark -i enp1s0 -n -b duration:$3 -b files:5  -y EN10MB -p -w ~/trafficLogs/enp1s0/M$1/enp1s0_M$1_$2.pcap  &

#Commands to extract the data at GW2
#scp -r jugaad@192.168.3.1:/home/trafficLogs ~/LOGS/Mal_Sample#<num>/
#drwxr-xr-x  2 root    root          4096 Mar 13 17:28  temp

