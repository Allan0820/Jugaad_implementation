import pika
import json
import os
import uuid
import psycopg2
credentials=pika.PlainCredentials('OMR_RMQ','Omr@123')
connection = pika.BlockingConnection(pika.ConnectionParameters('172.23.254.74', 5672,'/', credentials))
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


def pushqueue(fileuuid, jobid): 

    channel2=connection2.channel()
    channel2.queue_declare("queue_2")

    message = { 
        'File_uuid': str(fileuuid),
        'Jobid': jobid
    }
    channel2.basic_publish(exchange='',
                           routing_key='queue_2',
                           body=json.dumps(message))
    print("Message put into receiving (Report) queue")


def on_message_received(ch, method, properties, body):


    
    json_value=json.loads(body)
    filehash=json_value["File_Hash"]
    jobid=json_value["Job_Id"]
    print(f"received a new filehash= {filehash} and a new jobid = {jobid}")
    cursor.execute("update omr_data set job_status='processing' where job_id=%s",(jobid,))

    file_path='/home/omr/files/'+filehash
    
        # Call the shell script using subprocess.run
   # subprocess.call(['sh','./transfer.sh'])  uses a blocking call hence execution of the program will be halted.
    
    #python script for processing of the file 
    report_file_name=uuid.uuid1()
    
    stats = os.stat(file_path)
    file_size = stats.st_size
    permissions = oct(stats.st_mode & 0o777)
    last_mod_time = stats.st_mtime
    inode_number = stats.st_ino
    owner = stats.st_uid
    group = stats.st_gid
    file= open(f'/home/omr/report/{report_file_name}.txt','w')
    file.write(f'Welcome to file statistics for the file {filehash}\n\n')
    file.write('stats = '+str(stats)+'\n')
    file.write('permissions = '+permissions+'\n')
    file.write('last_mod_time = '+str(last_mod_time)+'\n')
    file.write('inode_number = '+str(inode_number)+'\n')
    file.write('owner = '+str(owner)+'\n')
    file.write('group = '+str(group)+'\n')
    file.close()    
    print("File processing complete")

    # after the file is received back to the gateway2 after processing by the profiler, it goes to the reports folder and a message is pushed into another queue 
    pushqueue(report_file_name, jobid)

    print("Job processing complete")
    
     
channel=connection.channel()

channel.queue_declare("queue_1")


channel.basic_consume(queue='queue_1', auto_ack=True, on_message_callback=on_message_received)

print("Starting the Pulling of messages to Gateway 2")

channel.start_consuming()


