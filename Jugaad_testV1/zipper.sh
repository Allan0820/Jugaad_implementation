#!/bin/bash
name=$1
# #zip /home/omrapp/Desktop/reporthash/${name}_NW.zip home/omrapp/Desktop/reporthash/trafficLogs
# echo "jug@@d*%$" | sudo -s chmod 777 home/omrapp/Desktop/reporthash/trafficLogs
# echo "jug@@d*%$" | sudo -s chmod 777  home/omrapp/Desktop/reporthash/trafficLogs/enp2s0_${name}.pcap

zip -j -r /home/omrapp/Desktop/reporthash/${name}.zip /home/omrapp/Desktop/reporthash/${name}.csv /home/omrapp/Desktop/reporthash/trafficLogs


rm -rf /home/omrapp/Desktop/reporthash/trafficLogs/*
