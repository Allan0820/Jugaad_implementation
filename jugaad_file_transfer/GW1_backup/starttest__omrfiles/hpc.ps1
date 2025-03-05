$s= New-PSSession -HostName abhinab@192.168.2.25
Invoke-Command -HostName abhinab@192.168.2.25 -ScriptBlock {

#winrs.exe -r:HPCMACHINE   mkdir D:\Project\new_naveen
winrs.exe -r:HPCMACHINE -u:abhinab -p:Omr@hpc2025 mkdir D:\Project\new_naveen

}


