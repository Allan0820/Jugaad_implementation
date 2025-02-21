import os 
import uuid
import pika 
import hashlib
import json
import psycopg2
from zipfile import ZipFile
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import zipfile

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import DeclarativeBase

from werkzeug.utils import secure_filename
from flask import Flask, render_template, request
#from flask_material import Material 

from flask_cors import CORS
app = Flask(__name__)
# Material(app)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024 
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
# app.config['UPLOAD_FOLDER']='/home/omrapp/lol/File_hash/'
app.config['UPLOAD_FOLDER']='/home/omrapp/Desktop/filehash/'

app.config['DEBUG']=True
app.config['TESTING']=False
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USE_SSL']=False
# app.config['MAIL_DEBUG']=True
app.config['MAIL_USERNAME']='allan.n.pais@gmail.com'
app.config['MAIL_SENDER']='allan.n.pais@gmail.com'
app.config['MAIL_PASSWORD']='fgyy axcd depv vexe'
app.config['MAIL_DEFAULT_SENDER']=None
app.config['MAIL_MAX_EMAILS']=None
# app.config['MAIL_SUPPRESS_SEND']=False
app.config['MAIL_ASCII_ATTACHMENTS']=False
#  app password   fgyy axcd depv vexe
# mail=Mail(app)

connection = psycopg2.connect(
                      database="omrdatabase", 
                      host="172.23.254.74", 
                      port=5432,
                      user="omruser",
                      password="Omr@123" ,
                    )

cursor=connection.cursor()
connection.autocommit=True 

# sql = '''select * from omr_data;'''

# cursor.execute(sql)

# print(list((cursor.fetchall()[0]))[2])



def pushqueue(filehash, jobid):
  

  credentials = pika.PlainCredentials('OMR_RMQ', 'Omr@123')
  connection = pika.BlockingConnection(pika.ConnectionParameters('172.23.254.74', 5672, '/',   credentials))

  channel =connection.channel()

  channel.queue_declare("queue_1")
  
  message = { 
               'File_Hash':filehash,
               'Job_Id':jobid      
            }
  
  
  channel.basic_publish(exchange='',
                      routing_key='queue_1',
                      body=json.dumps(message) )

  print("Message pushed to the queue")



@app.route("/")
def welcome():
    
    return render_template("fileupload.html")
     

@app.route('/fileupload', methods = ['GET'])
def send_upload():
    
    return render_template("fileupload.html")
    
@app.route('/filesend', methods = ['POST'])
def receive():
    print("The value of the path is  ",app.instance_path)
    if request.method == 'POST':
        print("inside")

        files = request.files['files']
        email = request.form['email'] 
        comments = request.form['comments']
        filename=secure_filename(files.filename)
        
        print(email)
        #os.makedirs(os.path.join(app.instance_path, 'Uploaded_files'))
        file_md5_hash=hashlib.md5(files.read()).hexdigest()
        filename=file_md5_hash
        print(filename)
        
        # run a database precheck 
        cursor.execute("select count(%s) from omr_data where file_hash=%s AND job_status='pending';",(filename,filename))
        pending_temp=list(cursor.fetchall()[0])[0] 
        cursor.execute("select count(%s) from omr_data where file_hash=%s AND job_status='processing';",(filename,filename))
        processing_temp=list(cursor.fetchall()[0])[0] 
        cursor.execute("select count(%s) from omr_data where file_hash=%s AND job_status='complete';",(filename,filename))
        complete_temp=list(cursor.fetchall()[0])[0] 
        # print("Number of rows are ",len(cursor.fetchall()))
        print(pending_temp)
        print(processing_temp)
        print(complete_temp)
        if ((pending_temp + processing_temp + complete_temp) == 0):
            

            files.seek(0) #getting the file pointer to the start 
        
            files.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            print("hi")
            with ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as myzip:
              myzip.write(filename)
            print("zipped")
            # changing file permissions 
            os.chmod(os.path.join(app.config['UPLOAD_FOLDER'],filename),0o666)
           

            cursor.execute("insert into omr_data values (DEFAULT,%s,%s,%s,NULL,'pending')",(email,filename,comments))
            
            cursor.execute("select job_id from omr_data where file_hash=%s AND job_status='pending';",(filename,))
            job_id=list(cursor.fetchall()[0])[0] 
            
            pushqueue(file_md5_hash, job_id)
            # file_md5_hash=""
            return "File pushed to the message queue successfully! Press back to continue"
        elif (pending_temp != 0):
            return "A similar file has been submitted and is awaiting processing, an email with the report for this file will be sent shortly OR Please try again later"    
        elif (processing_temp != 0):
            return "A similar file has been submitted and is currently processing, an email with the report for this file will be sent shortly OR Please try again later "  
        else :

            cursor.execute("select trail_hash from omr_data where file_hash=%s AND job_status='complete';",(filename))
            trail_hash=list(cursor.fetchall()[0])[0]
            # call to the send_email() function 
            return "A similar file has been processed and a report will be sent via email shortly"

        
 
@app.route('/upload_file/', methods=['POST'])
def upload_file():
        file = request.files['file']
if __name__=="__main__":
    # db.create_all()
    
    app.debug=True
    app.run()
