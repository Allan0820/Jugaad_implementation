#Must be the first statement in your script (not coutning comments)
param([string]$hash="dummy")

Write-Host "Starting the PowerShell script"

$session = New-PSSession -HostName jugaad@192.168.2.27
Write-Host "Connection Created  to run Malware -- >"

Write-Host $hash

Write-Host "Hello, World from the Profiler!"

Invoke-Command -Session $session -ScriptBlock {

Write-Host "C:\Profiler_OS_NW\malware_submission\$hash.dat"

Psexec.exe -i \\192.168.2.27 python "C:\Profiler_OS_NW\procmonallan.py" C:\Profiler_OS_NW\malware_submission\$hash.dat 5
Start-Sleep -s 5

Write-Host "Copying the CSV and PID file"

Write-Host "Copy CSV from profiler to gateway1"
sshpass -p "jug@@d*%$" scp jugaad@192.168.2.27:c:/Profiler_OS_NW/OS_Data_csv/"$hash.csv" /home/jugaad/OS_DataFromProfiler/
#scp jugaad@192.168.2.27:c:/Profiler_OS_NW/OS_Data_csv/"$hash.csv" /home/jugaad/OS_DataFromProfiler/
Write-Host "Copy CSV from gateway1 to gateway2"
#sshpass -p "jugaad" scp /home/jugaad/OS_DataFromProfiler/$Using:hash.csv jugaad@202.141.30.50:/home/omr/report
sshpass -p "jug@@d*%$" scp /home/jugaad/OS_DataFromProfiler/"$hash.csv" jugaad@202.141.30.50:/home/omr/report
#scp /home/jugaad/OS_DataFromProfiler/"$hash.csv" jugaad@202.141.30.50:/home/omr/report
Write-Host "CSV in /home/omr/report"

}
