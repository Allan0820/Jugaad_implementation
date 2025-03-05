import os 
from subprocess import *
import subprocess
# print Macs
def Get_Subnet_Health():
	IPs_file_name = "IPs.txt"
	IPs_file = open(IPs_file_name,"r")
	IPs = IPs_file.read().split("\n")
	IP_addresses = {}
	for machine in IPs:
		machine = machine.split("\t")
		#print machine
		IP_addresses[machine[0]] = machine[1]
	Subnet_Status = {}
	for machine in IP_addresses:
		machine_ip = IP_addresses[machine]
		cmd = "ping -c 2 "+machine_ip
		output = subprocess.Popen(["ping","-c","2",machine_ip], stdout=subprocess.PIPE).communicate()[0]
		#print output
		if "0% packet loss" in output:
			#print machine+" : OK"
			Subnet_Status[machine] = "OK"
		else:
			Subnet_Status[machine] = "NOT OK"
	#print Subnet_Status
	return Subnet_Status
