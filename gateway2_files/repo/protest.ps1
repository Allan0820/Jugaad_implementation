#Must be the first statement in your script (not coutning comments)
param([string]$hash="dummy")

Write-Host "Starting the PS script"

$session = New-PSSession -HostName jugaad@192.168.2.27
Write-Host "Connection Created  to run Malware -- >"

Write-Host $hash

$copyofRemotePID = 1

Invoke-Command -Session $session -ScriptBlock {
Write-Host "Hello, World from Profiler!"
Write-Host "Testing the malware on the profiler"
Write-Host $Using:hash

cd C:\Profiler_OS_NW\
#$Using:hash = "0000B97B3322E5792F8C88E01B4F4313"
echo $Using:hash
file_name = hash
# Run automate
Copy-Item C:\Profiler_OS_NW\omrmalwares\$Using:hash.dat C:\Profiler_OS_NW\$Using:hash.exe

mkdir C:\\Profiler_OS_NW\\OS_Data_csv\\
mkdir C:\\Profiler_OS_NW\\OS_Data_pml\\

#Starting Procmon
Write-Host "starting Procmon" $Using:hash
Write-Host "psexec.exe -i -d  \\192.168.2.27 python C:\Profiler_OS_NW\procmonControl.py start " $Using:hash "0"
#psexec.exe -i  -d \\192.168.2.27 python C:\Profiler_OS_NW\procmonControl.py start $Using:hash 0
Psexec.exe -sd \\192.168.2.27 procmon -accepteula -backingfile c:\Profiler_OS_NW\OS_Data_pml\$Using:hash.pml -quiet


#Start and Get the PID of the malware hash
Write-Host "C:\Profiler_OS_NW\PSTools\psexec.exe -accepteula -i -d \\192.168.2.27 C:\Profiler_OS_NW\$Using:hash.exe  2>&1"

$remotePID = C:\Profiler_OS_NW\PSTools\psexec.exe -accepteula -i -d -s \\192.168.2.27 C:\Profiler_OS_NW\$Using:hash.exe 2>&1
$remotePID = $remotePID |  Select-String 'process ID (\d+)' |    ForEach-Object {$_.Matches.Groups[1].Value}
$remotePID

if ("" -ne $remotePID)
{
        Write-Output "MALWARE STARTED"
}

$copyofRemotePID = $remotePID

#love

Write-Host "Waiting for two minutes"
#Wait for 2 minutes
Start-Sleep -s 5


Write-Host "Stopping Procmon  " $Using:hash  $remotePID
#Stop procmon, #Get all child processes, #Writes to a PID file which can be copied later for processing.
Write-Host "psexec.exe -i \\192.168.2.27 python C:\Profiler_OS_NW\procmonControl.py stop " $Using:hash $remotePID

#psexec.exe -i -d \\192.168.2.27 python C:\Profiler_OS_NW\procmonControl.py stop $Using:hash $remotePID

Psexec.exe -sd \\192.168.2.27 procmon -accepteula -terminate -quiet
Psexec.exe -sd \\192.168.2.27 procmon -openlog c:\Profiler_OS_NW\OS_Data_pml\$Using:hash.pml -saveas  c:\Profiler_OS_NW\OS_Data_csv\$Using:hash.csv
psexec.exe -i -d \\192.168.2.27 python C:\Profiler_OS_NW\procmonControl.py stop $Using:hash $remotePID

Start-Sleep -s 30



}


Write-Host "Copy the CSV and PID file"


sshpass -p "jugaad" scp jugaad@192.168.2.27:c:/Profiler_OS_NW/OS_Data_csv/*.csv /home/jugaad/OS_DataFromProfiler/
#sshpass -p "jugaad" scp /home/jugaad/OS_DataFromProfiler/$Using:hash.csv jugaad@202.141.30.50:/home/omr/report
sshpass -p "jug@@d*%$" scp /home/jugaad/OS_DataFromProfiler/"$hash.csv" jugaad@202.141.30.50:/home/omr/report

Write-Host "copy PID"
sshpass -p "jugaad" scp jugaad@192.168.2.27:c:/Profiler_OS_NW/*.pid /home/jugaad/PID_DataFromProfiler/

if ("" -ne $remotePID)
{	
	Write-Host "malware did nit run "
	echo $hash $copyofRemotePID >> malwaredidnotrun.txt
}
