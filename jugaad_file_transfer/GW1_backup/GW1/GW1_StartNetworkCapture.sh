# To Call from remot
# GW1_StartNetworkCapture.sh <malware_id>  <Run_id> <interval_of_running_in_seconds>
# Eg. ~/jugaad/Malware/GW1/GW1_StartNetworkCapture.sh 1 1 180

rm -rf ~/trafficLogs
mkdir ~/trafficLogs
mkdir ~/trafficLogs/eno1
mkdir ~/trafficLogs/eno1/M$1
mkdir ~/trafficLogs/enp1s0
mkdir ~/trafficLogs/enp1s0/M$1

#echo jug@@d*%$ | sudo -S chown root:root -R ~/trafficLogs

#sudo tshark -i enp0s31f6 -n -b interval:$3 -b files:2  -y EN10MB -p -w /home/sareena/trafficLogs/eno1/M$1/eno$1_$2.pcap &

tshark -i eno1 -n -b duration:$3 -b files:5  -y EN10MB -p -w ~/trafficLogs/eno1/M$1/eno1_M$1_$2.pcap &
tshark -i enp1s0 -n -b duration:$3 -b files:5  -y EN10MB -p -w ~/trafficLogs/enp1s0/M$1/enp1s0_M$1_$2.pcap  &



#Commands to extract the data at GW2
#scp -r jugaad@192.168.3.1:/home/trafficLogs ~/LOGS/Mal_Sample#<num>/
#drwxr-xr-x  2 root    root          4096 Mar 13 17:28  temp

