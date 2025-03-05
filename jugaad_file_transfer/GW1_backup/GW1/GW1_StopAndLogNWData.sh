#Kill the logging
# Call format
# ~/jugaad/Malware/GW1/GW1StopAndLogNWData.sh


#ps -ef | grep tshark | awk '{print $2}' | sudo xargs kill -9

killall -9 tshark

#ps -ef | grep "tshark -i eno1" | awk '{print $2}' | xargs kill -9
#ps -ef | grep "tshark -i enp1s0" | awk '{print $2}' | xargs kill -9

#scp -i ~/.ssh/id_rsa -r ~/trafficLogs jugaad@192.168.3.254:/home/jugaad/NetworkData/GW1/
#scp -i ~/.ssh/id_rsa -r ~/trafficLogs jugaad@192.168.3.254:/home/jugaad/NetworkData/GW1/
#scp -i ~/.ssh/id_rsa -r ~/trafficLogs jugaad@192.168.3.254:/home/jugaad/NetworkData/GW1/

#sshpass -p "jug@@d*%$" chmod 777 jugaad@192.168.3.254:/home/jugaad/NetworkData/GW1/trafficLogs
#sshpass -p "jug@@d*%$" chmod 777 jugaad@192.168.3.254:/home/jugaad/NetworkData/GW1/trafficLogs/*
chmod 777 ~/trafficLogs/*


sshpass -p "jug@@d*%$" scp -r ~/trafficLogs jugaad@202.141.30.50:/home/omr/reporthash/

#sshpass -p "jug@@d*%$" chmod 777 jugaad@202.141.30.50:/home/jugaad/NetworkData/GW1/trafficLogs

#sshpass -p "jug@@d*%$" chmod 777 jugaad@202.141.30.50:/home/jugaad/NetworkData/GW1/trafficLogs/*



