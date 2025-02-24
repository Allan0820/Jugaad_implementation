import subprocess
import pika
import json
import os
import time
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

def copyMalwareToGW1(filehash):
    script_path = "/home/omr/jugaad_file_transfer/shellScripts/copyMalware.sh"
    try:
        copy_call_with_args="/home/omr/jugaad_file_transfer/shellScripts/copyMalware.sh '%s'" % (str(filehash+".dat"))
        print("copyexecuted form gateway2 to gateway1 start")
        os.system(copy_call_with_args)
        print("copyexecuted form gateway2 to gateway1 end")
        # subprocess.call([script_path,filehash],check = True)
        print("copied malware to gw1")
    except subprocess.CalledProcessError as e:
        print("error in copying the malware")

'''
def run_remote_python(remote_host, remote_user, remote_directory, remote_python_script, python_arg):
    # Call the shell script and pass the necessary arguments
    subprocess.call([
        '/home/omr/jugaad_file_transfer/shellScripts/runStartTesh.sh',  # Path to the shell script
        remote_host,        # Remote host (IP or hostname)
        remote_user,        # Remote user
        remote_directory,   # Remote directory where Python script is located
        remote_python_script,  # Name of the Python script on the remote machine
        python_arg          # Argument to pass to the remote Python script
    ])
'''

'''
def run_remote_python(remote_host, remote_user, remote_directory, remote_python_script, python_arg):
    # Call the shell script and pass the necessary arguments
    process = subprocess.Popen([
        '/home/omr/jugaad_file_transfer/shellScripts/runStartTesh.sh',  # Path to the shell script
        remote_host,        # Remote host (IP or hostname)
        remote_user,        # Remote user
        remote_directory,   # Remote directory where the Python script is located
        remote_python_script,  # Name of the Python script on the remote machine
        python_arg          # Argument to pass to the remote Python script
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Continuously read and print output while the process is running
    while True:
        output = process.stdout.readline()
        if output == b'' and process.poll() is not None:
            break
        if output:
            print(output.decode().strip())  # Print the output to the terminal

    # Wait for the process to complete
    process.wait()
'''


def run_remote_python(remote_host, remote_user, remote_directory, remote_python_script, python_arg):
    print("Called the remote python function with arguments \n\n",remote_host,remote_user, remote_directory,remote_python_script,python_arg)
    
    copy_call_with_args="/home/omr/jugaad_file_transfer/shellScripts/runStartTesh.sh '%s' '%s' '%s' '%s' '%s'" % (str(remote_host),str(remote_user),str(remote_directory),str(remote_python_script),str(python_arg+".dat"))
    print("remote script invocation form gateway1 to profiler callstart")
    os.system(copy_call_with_args)
    print("remote script invocation form gateway1 to profiler callend")


    # try:
    #     # Call the shell script and pass the necessary arguments
    #     process = subprocess.call([
    #         '/home/omr/jugaad_file_transfer/shellScripts/runStartTesh.sh',  # Path to the shell script
    #         remote_host,        # Remote host (IP or hostname)
    #         remote_user,        # Remote user
    #         remote_directory,   # Remote directory where the Python script is located
    #         remote_python_script,  # Name of the Python script on the remote machine
    #         python_arg          # Argument to pass to the remote Python script
    #     ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    #     #Continuously read and print output while the process is running
    #     while True:
    #         output = process.stdout.readline()
    #         if output == b'' and process.poll() is not None:
    #             break
    #         if output:
    #             print(output.decode().strip())  # Print the output to the terminal

    #     # Read remaining stderr to avoid blocking
    #     stderr_output = process.stderr.read().decode()
    #     if stderr_output:
    #         print("Error:", stderr_output.strip())
    #         print("There is an error that has occured")
    #     # Ensure process completes without affecting the main script
    #     process.communicate()

    # except Exception as e:
    #     print("An error occurred:", str(e))

    #Function returns, allowing the main script to continue


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
#    cursor.execute("update omr_data set job_status='processing' where job_id=%s",(jobid,))

    file_path='/home/omr/files/'+filehash+".dat"
    
    try:
        copyMalwareToGW1(filehash)
    except Exception as e:
        print("error  Occured in the malware copy script ")
        exit(0)
        # Call the shell script using subprocess.run
   # subprocess.call(['sh','./transfer.sh'])  uses a blocking call hence execution of the program will be halted.
    try:
        run_remote_python("192.168.3.1", "jugaad","/home/jugaad/jugaad/Malware/GW1/startTest/omrFiles", "remotestartTestV2.py", filehash)
    #python script for processing of the file 
    except Exception as e:
        print("error in running script")    

    # after the file is received back to the gateway2 after processing by the profiler, it goes to the reports folder and a message is pushed into another queue 
    pushqueue(filehash, jobid)

    print("Job processing complete")
    ch.basic_ack(delivery_tag=method.delivery_tag)
    
     
channel=connection.channel()

channel.queue_declare("queue_1")


channel.basic_consume(queue='queue_1', auto_ack=False, on_message_callback=on_message_received)

print("Starting the Pulling of messages to Gateway 2")

channel.start_consuming()


