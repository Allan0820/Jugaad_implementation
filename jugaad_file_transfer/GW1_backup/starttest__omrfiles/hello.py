print("Hello from the Profiler!")
print("\n")
print("################# PROCMON") 
print("\n")

import os
import subprocess
import time
from time import sleep
import sys

#PMC = str(sys.argv[2]) to set PMC file argument
name = str(sys.argv[1])
TIMEOUT = int(sys.argv[2])
PMC="False"
pmc_file = r""
procmon_path = r"C:\\Profiler_OS_NW\\ProcessMonitor\\Procmon.exe"
execute_file = r"C:\\Profiler_OS_NW\\malware_submission\\" + name + ".exe"      
csv_file_path = os.path.expandvars(r"C:\\Profiler_OS_NW\\OS_Data_csv\\" + name + ".csv")
pml_file_path = os.path.expandvars(r"C:\\Profiler_OS_NW\\OS_Data_pml\\" + name + ".pml")

time_exec, time_process, time_analyze = 0, 0, 0

#start the procmon

time_exec=time.time()
cmdline = '"%s" /AcceptEula /NoFilter /BackingFile "%s" /Quiet /Minimized' % (procmon_path, pml_file_path)

print("--> Starting Procmon Capture \n")

if PMC:
   cmdline += ' /LoadConfig "%s"' % pmc_file

print('------> Running cmdline command : %s' % cmdline)
p1 = subprocess.Popen(cmdline, shell=True)

sleep(TIMEOUT)
time_exec=time.time()-time_exec

cmdline = '"%s" /Terminate' % procmon_path
print("--> Stopping Procmon Capture \n")
print('------> Running cmdline command : %s' % cmdline)
#p2= subprocess.Popen(cmdline, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
p2= subprocess.Popen(cmdline, shell=True)
p2.wait()
#os.killpg(os.getpid(p2.pid), signal.SIGTERM)

#finally convert everything to a csv file
time_process=time.time()
print('--> Converting session to CSV: %s' % csv_file_path)
cmdline = '"%s" /OpenLog "%s" /saveas "%s"' % (procmon_path, pml_file_path, csv_file_path)
if PMC:
    cmdline += ' /LoadConfig "%s"' % pmc_file
print('------> Running cmdline: %s' % cmdline)
#p3= subprocess.Popen(cmdline, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
p3= subprocess.Popen(cmdline, shell=True)
p3.wait()
#os.killpg(os.getpid(p3.pid), signal.SIGTERM)
time_process = time.time() - time_process
print('################# PROCMON FINISHED SUCCESSFULLY######################') 
print("\n")
print("################# PROCMON ")
print("\n")

