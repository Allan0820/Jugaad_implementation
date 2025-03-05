#Kill the logging
# Call format
# ~/jugaad/Malware/GW1/GW1StopAndLogNWData.sh


#ps -ef | grep tshark | awk '{print $2}' | sudo xargs kill -9

#killall -9 tshark
ps -ef | grep "tshark -i enp2s0" | awk '{print $2}' | xargs kill -9

scp -i ~/.ssh/id_rsa -r ~/trafficLogs41/enp2s0 jugaad@192.168.3.254:/home/jugaad/NetworkData/GW1/
