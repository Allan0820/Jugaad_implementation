#Must be the first statement in your script (not coutning comments)
param([string]$hash="dummy")

Write-Host "Starting the PS script"

$session = New-PSSession -HostName jugaad@192.168.2.27
Write-Host "Connection Created  to run Malware -- >"

Write-Host $hash

$copyofRemotePID = 1

Invoke-Command -Session $session -ScriptBlock {
Write-Host "Hello, World from the Profiler!"
Write-Host "Running the malware on the profiler"
Write-Host $Using:hash

cd C:\Profiler_OS_NW\
#$hash1, $ext = $hash.split(".")

#Write-Host "The changed hash value for processing in the protest.ps1 file is"
#Write-Host $hash1

file_name = hash
# Run automate
Copy-Item C:\Profiler_OS_NW\omrmalwares\$Using:hash.dat C:\Profiler_OS_NW\$Using:hash.exe

#get-childitem *.dat | foreach { rename-item $_ $_.Name.Replace(".dat",".exe")}
# here is where the filetype is getting converted from hash.dat to hash.exe 

# Making the directories on the system for the storage of the trails.
#mkdir C:\\Profiler_OS_NW\\OS_Data_csv\\
#mkdir C:\\Profiler_OS_NW\\OS_Data_pml\\
#$hash = [System.IO.Path]::GetFileNameWithoutExtension($hash)
#Starting Procmon
Write-Host "starting Procmon" $Using:hash
#change made to the below line
Write-Host "psexec.exe -i -d  \\192.168.2.27 python C:\Profiler_OS_NW\procmonControl copy.py start " $Using:hash.exe
Psexec.exe -i  -d \\192.168.2.27 python "C:\Profiler_OS_NW\procmonControl.py" start C:\Profiler_OS_NW\$Using:hash.exe


#here the procmon is actully processing the results.
Start-Sleep -s 15 



#Psexec.exe -i -d \\192.168.2.27 python "C:\Profiler_OS_NW\procmonControl copy.py" stop $Using:hash.exe $remotePID
#Psexec.exe -sd \\192.168.2.27 procmon -accepteula -backingfile c:\Profiler_OS_NW\OS_Data_pml\$Using:hash.pml -quiet


#Start and Get the PID of the malware hash
Write-Host "C:\Profiler_OS_NW\PSTools\psexec.exe -accepteula -i -d \\192.168.2.27 C:\Profiler_OS_NW\$Using:hash.exe  2>&1"

$remotePID = C:\Profiler_OS_NW\PSTools\psexec.exe -accepteula -i -d -s \\192.168.2.27 C:\Profiler_OS_NW\$Using:hash.exe 2>&1
$remotePID = $remotePID |  Select-String 'process ID (\d+)' |    ForEach-Object {$_.Matches.Groups[1].Value}
$remotePID

Psexec.exe -i -d \\192.168.2.27 python "C:\Profiler_OS_NW\procmonControl.py" stop C:\Profiler_OS_NW\$Using:hash.exe

Psexec.exe -sd \\192.168.2.27 procmon -accepteula -backingfile c:\Profiler_OS_NW\OS_Data_pml\$Using:hash.pml -quiet




if ("" -ne $remotePID)
{
        Write-Output "Malware Execution has started"
}

$copyofRemotePID = $remotePID


Write-Host "Waiting for two minutes"
#Wait for 2 minutes
Start-Sleep -s 3


Write-Host "Stopping Procmon with the identified hash and PID" $Using:hash  $remotePID
#Stop procmon, #Get all child processes, #Writes to a PID file which can be copied later for processing.
Write-Host "psexec.exe -i \\192.168.2.27 python C:\Profiler_OS_NW\procmonControl.py stop " $Using:hash.exe $remotePID

#psexec.exe -i -d \\192.168.2.27 python "C:\Profiler_OS_NW\procmonControl.py" stop $Using:hash $remotePID

#psexec.exe -sd \\192.168.2.27 procmon -accepteula -terminate -quiet
Write-Host "Writing the trails on the profiler to Profiler OS_Data_csv"
psexec.exe -sd \\192.168.2.27 procmon -openlog c:\Profiler_OS_NW\OS_Data_pml\$hash.pml -saveas  c:\Profiler_OS_NW\OS_Data_csv\$hash.csv
Write-Host "Finished writing the trails on the profiler to Profiler OS_Data_csv"

#psexec.exe -i -d \\192.168.2.27 python C:\Profiler_OS_NW\procmonControl.py stop $hash $remotePID 

Start-Sleep -s 2


}

#$hash = $hash -replace '\.dat$', ''
Write-Host "Copying the CSV and PID file"

Write-Host "Copy CSV from profiler to gateway1"
sshpass -p "jug@@d*%$" scp jugaad@192.168.2.27:c:/Profiler_OS_NW/OS_Data_csv/"$hash.csv" /home/jugaad/OS_DataFromProfiler/
#scp jugaad@192.168.2.27:c:/Profiler_OS_NW/OS_Data_csv/"$hash.csv" /home/jugaad/OS_DataFromProfiler/
Write-Host "Copy CSV from gateway1 to gateway2"
#sshpass -p "jugaad" scp /home/jugaad/OS_DataFromProfiler/$Using:hash.csv jugaad@202.141.30.50:/home/omr/report
sshpass -p "jug@@d*%$" scp /home/jugaad/OS_DataFromProfiler/"$hash.csv" jugaad@202.141.30.50:/home/omr/report
#scp /home/jugaad/OS_DataFromProfiler/"$hash.csv" jugaad@202.141.30.50:/home/omr/report
Write-Host "CSV in /home/omr/report"

Write-Host "copy PID"
sshpass -p "jugaad" scp jugaad@192.168.2.27:c:/Profiler_OS_NW/*.pid /home/jugaad/PID_DataFromProfiler/
#scp jugaad@192.168.2.27:c:/Profiler_OS_NW/*.pid /home/jugaad/PID_DataFromProfiler/

if ("" -ne $remotePID)
{	$session = New-PSSession -HostName jugaad@192.168.2.27
	Write-Host "malware did not run"
       # psexec.exe -i -d \\192.168.2.27 cd C:\Profiler_OS_NW\OS_Data_csv\

        #$filePath = "C:\Profiler_OS_NW\OS_Data_csv\$hash.csv"
       # psexec.exe -i -d \\192.168.2.27 Set-Content -Path "$hash.csv" -Value "The file that you have sent could not be run, please try again."       
	echo $hash $copyofRemotePID >> malwaredidnotrun.txt
}
