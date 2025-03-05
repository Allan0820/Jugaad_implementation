param([string]$hash="dummy")

$s = New-PSSession -HostName 192.168.2.27 -UserName jugaad -SSHTransport

#$s= New-PSSession -HostName jugaad@192.168.2.27
#$s= New-PSSession -ComputerName DESKTOP-JU2JP09
#Invoke-Command -HostName jugaad@192.168.2.27 -ScriptBlock {
#winrs.exe -r:DESKTOP-JU2JP09 python C:\Profiler_OS_NW\procmonallan.py $Using:hash 5
#}

#sshpass -p "jug@@d*%$" scp jugaad@192.168.2.27:c:/Profiler_OS_NW/OS_Data_csv/"$hash.csv" /home/jugaad/jugaad/temp_trail_storage/
#sshpass -p "jug@@d*%$" scp /home/jugaad/jugaad/temp_trail_storage/"$hash.csv" jugaad@202.141.30.50:/home/omr/reporthash/

#rm /home/jugaad/jugaad/temp_trail_storage/$hash.csv











#sshpass -p "jug@@d*%$" zip "$hash.zip" omr@202.141.30.50:/home/omr/temp_trail_storage/"$hash.csv"

#sshpass -p "jug@@d*%$" scp omr@202.141.30.50:/home/omr/temp_trail_storage/$hash.csv /home/omr/reporthash/


#$s= New-PSSession -HostName jugaad@192.168.2.27
#Invoke-Command -HostName jugaad@192.168.2.27 -ScriptBlock {

#winrs.exe -r:DESKTOP-HSVHQL shutdown /r 

#}

