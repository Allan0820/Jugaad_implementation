import pika
import json
import os
import uuid
import psycopg2
import smtplib
import smtplib
import subprocess
import shlex
from pradar import network_scripts_production_ready, os_scripts_production_ready
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
credentials=pika.PlainCredentials('OMR_RMQ','Omr@123')
connection2 = pika.BlockingConnection(pika.ConnectionParameters('172.23.254.74', 5672,'/', credentials))

connection1 = psycopg2.connect(
                      database="omrdatabase", 
                      host="172.23.254.74", 
                      port=5432,
                      user="omruser",
                      password="Omr@123" ,
                    )
cursor=connection1.cursor()
connection1.autocommit=True 

def enterTH(job_id , trailHash):
    query="update malware_table set status = %s,trailhash = %s where job_id = %s"
    query2="select * from malware_table where job_id = %s"
    cursor.execute(query,(2,trailHash,job_id,))
    result = cursor.fetchone
    if result:
        cursor.execute(query2,(job_id,))
        result2 = cursor.fetchone()
        Job_id = result2[0]
        return Job_id
        
    else:
        return -1

def getUIDS(job_id):
    query = "SELECT user_id FROM request_table WHERE job_id = %s"
    cursor.execute(query, (job_id,))
    result = cursor.fetchall()  # Fetch all matching rows

    if result:
        # Extract user_ids from the result tuples
        user_ids = [row[0] for row in result]  # row[0] gets the user_id from each tuple
        return user_ids
    else:
        return [-1]  # Return [-1] if no results are found

def getEmail(user_ids):
    # Create placeholders for each user_id in the tuple
    placeholders = ', '.join(['%s'] * len(user_ids))
    query = f"SELECT email FROM user_table WHERE user_id IN ({placeholders})"

    # Execute the query with the tuple of user_ids
    cursor.execute(query, user_ids)  # user_ids is already a tuple
    result = cursor.fetchall()  # Fetch all matching rows

    if result:
        # Extract emails from the result tuples
        emails = [row[0] for row in result]  # row[0] gets the email from each tuple
        return emails
    else:
        return [""]  # Return an empty string if no results are found

def on_message_received(ch, method, properties, body):

    json_value=json.loads(body)
    report_file_name=json_value["File_uuid"]#trailhash 
    job_id=json_value["Jobid"]
    enterTH(job_id,report_file_name)
    user_ids = getUIDS(job_id)
    email_id = getEmail(user_ids)
    # email_id.append("21f1001663@ds.study.iitm.ac.in")

    if email_id == "":
        email_id="allaniitm0820@gmail.com"
    
    print(f"received a new filehash= {report_file_name} and a new job id = {job_id}")
    report_path=f'/home/omrapp/Desktop/reporthash/{report_file_name}.csv'

    for emails in email_id:
        subject=f"Greetings {emails}! Open Malware Research has processed your report!"

        body=f'''Dear {emails},

        I hope this email finds you well. Please find the runtime trails attached for your review.

        We appreciate your continued trust in the Open Malware Research Service. If you have any further questions or require additional assistance, feel free to reach out.

        Thank you for choosing our services.

        Best regards,
        OpenMalwareResearch'''


        sender_email="allan.n.pais@gmail.com"
        password='fgyy axcd depv vexe'
        smtp_server='smtp.gmail.com'
        sender_password='fgyy axcd depv vexe'
        smtp_port=587

        print("Starting the RaDAR purification")
        print("Compiling the OS + Network files")
        network_scripts_production_ready.zeek_process(report_file_name)
        os_scripts_production_ready.os_scripts(report_file_name)
        print("Ended the RaDAR purification")
        os.system("zip -j /home/omrapp/Desktop/reporthash/"+"radar_processed_"+report_file_name+".zip /home/omrapp/Desktop/reporthash/radar_processed_ostrails_"+report_file_name+".csv /home/omrapp/Desktop/reporthash/radar_processed_networktrails_"+report_file_name+".csv")
        os.system("rm /home/omrapp/Desktop/reporthash/*.csv")
        # os.system("mv /home/omrapp/Desktop/reporthash/returned_os_logs/*.csv /home/omrapp/Desktop/reporthash/raw_os")
        # os.system("mv /home/omrapp/Desktop/reporthash/returned_network_logs/*.pcap /home/omrapp/Desktop/reporthash/raw_network")

        # try:
        message = MIMEMultipart()
        message['Subject']=subject
        message['From']=sender_email
        message['To']=emails
        
        files=[f'/home/omrapp/Desktop/reporthash/radar_processed_{report_file_name}.zip']

        message.attach(MIMEText(body))

        for f in files :
            with open(f, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=basename(f)
                )
                
                part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
                message.attach(part)

        smtp = smtplib.SMTP(smtp_server, 587)
        smtp.starttls()
        smtp.login(sender_email,password)
        smtp.sendmail(sender_email, emails, message.as_string())
        smtp.close()
        cursor.execute("update malware_table set status=1 where job_id=%s",(job_id,))
        print("Email Sent!")
        # except: 
        #     message = MIMEMultipart()
        #     message['Subject']=subject
        #     message['From']=sender_email
        #     message['To']=emails
        #     message.attach(MIMEText(f'''Dear {emails},

        # There has been an error encountered during the processing of your job. Please try again. 
        # We sincerely apologize for the inconvenience caused.Please submit your 
        # job again 

        # Best regards,
        # OpenMalwareResearch'''))

        #     smtp = smtplib.SMTP(smtp_server, 587)
        #     smtp.starttls()
        #     smtp.login(sender_email,password)
        #     smtp.sendmail(sender_email, emails, message.as_string())
        #     smtp.close()
        #     print("Error Email sent")
        ch.basic_ack(delivery_tag=method.delivery_tag)   
        
        


channel=connection2.channel()

channel.queue_declare("queue_2")


channel.basic_consume(queue='queue_2', auto_ack=False, on_message_callback=on_message_received)

print("Starting the sending of emails")

channel.start_consuming()
