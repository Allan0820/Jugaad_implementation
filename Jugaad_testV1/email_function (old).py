import pika
import json
import os
import uuid
import psycopg2
import smtplib
import smtplib
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

def on_message_received(ch, method, properties, body):

    json_value=json.loads(body)
    report_file_name=json_value["File_uuid"]
    jobid=json_value["Jobid"]
    print(f"received a new filehash= {report_file_name} and a new jobid = {jobid}")
    #report_path=f'/home/omrapp/Desktop/{report_file_name}.txt'
    
    cursor.execute("select user_email from omr_data where job_id=%s",(jobid,))
    email_id=list(cursor.fetchall()[0])[0]
    subject=f"Greetings {email_id}! Open Malware Research has processed your report!"

    body=f'''Dear {email_id},

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

    message = MIMEMultipart()
    message['Subject']=subject
    message['From']=sender_email
    message['To']=email_id 

    files=[f'/home/omrapp/Desktop/reporthash/{report_file_name}.txt']

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
    smtp.sendmail(sender_email, email_id, message.as_string())
    smtp.close()
    cursor.execute("update omr_data set job_status='completed' where job_id=%s",(jobid,))
    print("Email Sent!")



channel=connection2.channel()

channel.queue_declare("queue_2")


channel.basic_consume(queue='queue_2', auto_ack=True, on_message_callback=on_message_received)

print("Starting the sending of emails")

channel.start_consuming()