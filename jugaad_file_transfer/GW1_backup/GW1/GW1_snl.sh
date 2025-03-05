#Kill the logging
# Call format
# ~/jugaad/Malware/GW1/GW1StopAndLogNWData.sh


#ps -ef | grep tshark | awk '{print $2}' | sudo xargs kill -9

#killall -9 tshark
ps -ef | grep "tshark -i eno1" | awk '{print $2}' | xargs kill -9
ps -ef | grep "tshark -i enp1s0" | awk '{print $2}' | xargs kill -9
sshpass -p 'omr@jug@@d*%$' scp -r ~/trafficLogs/eno1 omr@192.168.3.254:/home/omr/report
sshpass -p 'omr@jug@@d*%$' scp -r ~/trafficLogs/enp1s0 omr@192.168.3.254:/home/omr/report


#sshpass -p 'omr@jug@@d*%$' scp -r ~/trafficLogs/eno1 omr@192.168.3.254:/home/omr/report
#sshpass -p 'omr@jug@@d*%$' scp -r ~/trafficLogs/enp1s0 omr@192.168.3.254:/home/omr/report
#scp -i ~/.ssh/id_rsa -r ~/trafficLogs/eno1 jugaad@192.168.3.254:/home/jugaad/NetworkData/GW1/
#scp -i ~/.ssh/id_rsa -r ~/trafficLogs/enp1s0 jugaad@192.168.3.254:/home/jugaad/NetworkData/GW1/
