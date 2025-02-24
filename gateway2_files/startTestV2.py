import os
import glob
import shutil
import pandas as pd
import time
import subprocess
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import sys
import time


def sendmail():
    mail_content = '''Profilesr 1 SSH Connectin reset by peer. Need to look into this. Killed the test in the meantime'''
    # The mail addresses and password

    sender_address = 'malwarelabiitm@gmail.com'
    sender_pass = 'r!s!ngjug@@d$))'
    receiver_address_list = ['mailme.nikhilesh@gmail.com', 'sareena.kp@gmail.com ']
    # cc_address = "nik@cse.iitm.ac.in"
    for receiver_address in receiver_address_list:
        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'There is a crash.'  # subject
        # message['Cc'] = cc_address
        # The body and the attachments for the mail
        message.attach(MIMEText(mail_content, 'plain'))

        # Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587)  # gmail with port
        session.starttls()  # enable security
        session.login(sender_address, sender_pass)  # login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print('Mail Sent')





try:
    from subprocess import DEVNULL # Python 3
except ImportError:
    DEVNULL = open(os.devnull, 'r+b', 0)

print("Starting the test for the pending files")
pending = pd.read_csv("pendinglist.txt", index_col=[0])

completed = []
i = 0
for index, row in pending.iterrows():



    print("Stop prior tsharks and restart" )
    os.system("killall -9 tshark")

    response = 0

    #response = os.system('sshpass -p "jugaad" ssh -o StrictHostKeyChecking=no jugaad@192.168.2.27 shutdown /r')

    if response == 65280:
        print ("Ok an error - so send mail")
        sendmail()
        break;

    time.sleep(10)


    response = os.system("ping -c 1 192.168.2.27" )

    if response != 0:
        print ("Ok an error - so send mail")
        sendmail()
        break;


    #os.system('rm ~/OS_DataFromProfiler/' + str(row['hash']) + '*.csv')

    print(str(i) + ". " + row['hash'])

    if (row['hash'] in completed):
        continue

    file = str(row['hash'])

    file = file.strip(' ')


    i = i + 1

    ### NETLOG COMMANDS###

    ### NETLOG COMMANDS###
    netlog_cmd1_start_GW1_I1 = "echo \"jug@@d*%$\" |  /home/jugaad/jugaad/Malware/GW1/GW1_StartNetworkCapture.sh "
    netlog_cmd1_start_GW1_I2 = "echo \"jug@@d*%$\" |  /home/jugaad/jugaad/Malware/GW1/GW1_StartNetworkCapture_I2.sh "
    netlog_cmd5_stop_GW1 = "echo \"jug@@d*%$\" |  /home/jugaad/jugaad/Malware/GW1/GW1_StopAndLogNWData.sh"

    print("Start network cpture")
    ### Start the Network Capture in GW1 and GW2 ###
    os.system(netlog_cmd1_start_GW1_I1 + file + " 1 300")
    os.system(netlog_cmd1_start_GW1_I2 + file + " 1 300")




    print("\nStarting the Power Shell Script")
    #os.system('sshpass -p "jugaad" ssh -o StrictHostKeyChecking=no jugaad@192.168.2.38 C:/Profiler_OS_NW/automate_OS_NW.bat ' + str(row['hash']))

   # p = subprocess.Popen(["/usr/bin/pwsh",  "/home/jugaad/jugaad/Malware/GW1/startTest/protest.ps1", file ],stdout=sys.stdout)
    
    p = subprocess.Popen(["/usr/bin/pwsh",  "/home/jugaad/jugaad/Malware/GW1/startTest/protest.ps1", file],stdin=DEVNULL,stdout=sys.stdout)

    p.communicate()


    print("\n")


    ## 0000B97B3322E5792F8C88E01B4F4313

    print("\n")
    print("Procmon done")
    print("Stop the netwokr capture\n")

    time.sleep(20)
    os.system("sshpass -p jugaad scp jugaad@192.168.2.27:c:/Profiler_OS_NW/OS_Data_csv/*.csv /home/jugaad/OS_DataFromProfiler/")

    os.system ("sshpass -p jugaad scp jugaad@192.168.2.27:c:/Profiler_OS_NW/*.pid /home/jugaad/PID_DataFromProfiler/")


    ### Stop the network capture and transfer filer to GW1/NetworkData
    os.system(netlog_cmd5_stop_GW1)

    completed.append (file)
    completeddf = pd.DataFrame(completed)
    completeddf.to_csv("CompletedHashes.csv")

    print("Completed " + str(row['hash']))
    print("-------------------------------------------------------------------------")
    print("\n")
    #if (i > 1):
    #break

# time.sleep (10)

#subprocess.Popen(    'sshpass -p "jug@@d*%$" scp -i ~/.ssh/id_rsa -r /home/jugaad/OS_DataFromProfiler/*.csv jugaad@192.168.3.254:/home/jugaad/NetworkData/OSData/')

#subprocess.Popen(    'sshpass -p "jugaad" scp jugaad@192.168.2.38:c:/Profiler_OS_NW/*.pid /home/jugaad/PID_DataFromProfiler/')


completeddf = pd.DataFrame(completed)
completeddf.to_csv("CompletedHashes.csv")

