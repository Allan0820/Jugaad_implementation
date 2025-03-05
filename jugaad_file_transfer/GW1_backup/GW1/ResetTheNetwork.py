import os
import subprocess

def Reset_Subnet():
	Credentials_file_name = "Subnet_Passwords.txt"
	Credentials_file = open(Credentials_file_name,"r")

	Credentials = Credentials_file.read().split("\n")

	Username_Passwords  = {}
	for crd in Credentials:
		print crd
		crd = crd.split("\t")
		print crd
		username = crd[0]
		password = crd[1]
		Username_Passwords[username] = password
	print "Rebooting subnet....************......."
	for user in Username_Passwords:
		cmd = "sshpass -p "+Username_Passwords[user]+" ssh "+user+" shutdown -r -f -t 0"
		print "Rebooting machine: "+user
		subprocess.call(cmd,shell=True)
	subprocess.call("sleep 10",shell=True)
	print "Done reset of subnet..........**********......"
