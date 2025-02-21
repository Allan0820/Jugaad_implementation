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
import datetime
import datetime
import time
import smtplib
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, jsonify, flash 
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, session, url_for, redirect
from flask_session import Session
from authlib.integrations.flask_client import OAuth
from requests_oauthlib import OAuth2Session
from apikey import *

from flask_cors import CORS
app = Flask(__name__)
app.config["SESSION_PERMANENT"]=False
app.config["SESSION_TYPE"] = "filesystem"

app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024 
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
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
app.config['SECRET_KEY']=SECRET_KEY
#  app password   fgyy axcd depv vexe
# mail=Mail(app)
Session(app)
oauth=OAuth(app)
google = oauth.register(
     name='google',
     client_id=CLIENT_ID,
     client_secret=CLIENT_SECRET,
     server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
     client_kwargs={'scope':'openid profile email'},
     #authorize_url='https://accounts.google.com/o/oauth2/auth',
     #access_token_url = 'https://accounts.google.com/o/oauth2/token'
    
)

connection = psycopg2.connect(
                      database="omrdatabase", 
                      host="172.23.254.74", 
                      port=5432,
                      user="omruser",
                      password="Omr@123" ,
                    )

cursor=connection.cursor()
connection.autocommit=True 

# cursor2=connection.cursor()
# connection.autocommit=True 

# sql = '''select * from omr_data;'''

# cursor.execute(sql)

# print(list((cursor.fetchall()[0]))[2])

credentials=pika.PlainCredentials('OMR_RMQ','Omr@123')
connection2 = pika.BlockingConnection(pika.ConnectionParameters('172.23.254.74', 5672,'/', credentials))

def direct_mail_sent(emails,file_hash):

#    json_value=json.loads(body#)
    report_file_name=file_hash
    #report_path=f'/home/omrapp/Desktop/{report_file_name}.txt'
    
   
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

    message = MIMEMultipart()
    message['Subject']=subject
    message['From']=sender_email
    message['To']=emails 

    files=[f'/home/omrapp/Desktop/reporthash/{file_hash}.txt']

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
    print("Email Sent!")

def update_email_list(cursor, file_hash, email):
    query_elist = """
    UPDATE omr_data
    SET email_list = array_append(email_list, %s)
    WHERE file_hash = %s;
    """
    cursor.execute(query_elist, (email, file_hash))

def check_file_status(email):
    cursor=connection.cursor()
    connection.autocommit=True 

    # Query to count the number of records with the specified conditions
    query = """
        SELECT COUNT(*)
        FROM omr_data
        WHERE user_email = %s
        AND (job_status = 'pending' OR job_status = 'processing')
    """

    # Execute the query
    cursor.execute(query, (email,))

    # Fetch the result
    count = cursor.fetchone()[0]
    print("Count:", count)
    # Check the count and return the appropriate message
    if count >= 2:
        print("Your two files are already under processing/pending, kindly wait till they get processed and submit it later.")
        return 1;
    else:
    	return 0;


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
#---------------------------------Newly Designed Function ----------------------------------------------------------------------

def User_Check(email):
    # Check if the user already exists in the User_Table
    query_check = "SELECT User_Id, NOR FROM User_Table WHERE Email = %s;"
    cursor.execute(query_check, (email,))
    result = cursor.fetchone()

    if result:
        # User exists, extract User_Id and current NOR
        user_id = result[0]
        current_nor = result[1]
        
        # Increment NOR (Number of Requests)
        new_nor = current_nor + 1
        query_update_nor = "UPDATE User_Table SET NOR = %s WHERE User_Id = %s;"
        cursor.execute(query_update_nor, (new_nor, user_id))
        
        # Return the existing User_Id
        return user_id
    else:
        # User does not exist, insert new user with unique User_Id based on reduced timestamp
        current_time = int(time.time() * 1000)  # Use milliseconds since epoch, fits within BIGINT

        # Insert new user into the User_Table
        query_insert = """
        INSERT INTO User_Table (User_Id, Email, Date, NOR)
        VALUES (%s, %s, CURRENT_TIMESTAMP, 1);  -- New user, so NOR starts at 1
        """
        cursor.execute(query_insert, (current_time, email))

        # Return the newly generated User_Id
        return current_time


def checkMalware(filehash):
	query = "select * from malware_table where filehash = %s"
	cursor.execute(query,(filehash,))
	result = cursor.fetchone()
	if result:
		jobId = result[0]
		trail = result[2]
		status= result[4]
		return  status,trail,jobId
	else:
		return -1,-1,-1
		

def enterMalware(filehash , user_id):
	query="insert into malware_table (filehash,user_id) values(%s,%s)"
	query2="select * from malware_table where filehash = %s"
	cursor.execute(query,(filehash,user_id,))
	result = cursor.fetchone
	if result:
		cursor.execute(query2,(filehash,))
		result2 = cursor.fetchone()
		Job_id = result2[0]
		return Job_id
		
	else:
		return -1

def setReq(user_id , job_id, comment):
	query = "insert into request_table (user_id , job_id,comment)values(%s , %s , %s)"
	cursor.execute(query,(user_id,job_id,comment))
	result = cursor.fetchone
	if result:
		return 1
	else:
		return 0
#-------------------------------------------Newly Designed Function Ends----------------------------------------------------------------------	
username_list=[]

@app.route("/")
def welcome():
    
    #return render_template("index.html")
    return redirect(url_for('login_google'))
    
     

@app.route("/login/google")
def login_google():
    
    try:
    
        redirect_uri=url_for('authorize_google', _external=True)
        return google.authorize_redirect(redirect_uri)
    
    except Exception as e:
         
         print("There was an error in the google authentication")
         return f"Error occoured during login {str(e)}", 500


@app.route("/authorize/google")
def authorize_google():
     global username_list
     token = google.authorize_access_token()
     #token='https://accounts.google.com/o/oauth2/token'
     print("This is the token",token)
     userinfo_endpoint=google.server_metadata['userinfo_endpoint']
     resp = google.get(userinfo_endpoint)
     user_info = resp.json()
     username = user_info['email']
     username_list.append(username)
     session["username"]=username 
     session["oauth_token"]=token
     
     return redirect(url_for('send_upload'))


@app.route('/fileupload', methods = ['GET'])
def send_upload():
    
    return render_template("index.html")



@app.route('/filesend', methods = ['POST'])
def receive():
    print("The value of the path is  ",app.instance_path)
    if request.method == 'POST':
        #print("inside")

        try:
            files = request.files['files']
        except KeyError:
            return "Missing 'name' key in the form!"
	
#        files = request.files['files']
        email = request.form['email'] 
        #now here we will check whether the user exist here or not 
        user_id = User_Check(email)
        
        
        comments = request.form['comments']
        filename=secure_filename(files.filename)
        #os.makedirs(os.path.join(app.instance_path, 'Uploaded_files'))
        file_md5_hash=filename 
        file_md5_hash=hashlib.md5(files.read()).hexdigest()
        filename=file_md5_hash+".dat" # since we have a file that needs to be accepted in the dat format which is then converted to .exe
        #removed the .dat extension
       
        #now here we have to check the status of the malware 
        status,trail,job_id = checkMalware(filename)
        
        if status !=-1 and trail!=-1 and job_id!=-1:
            setReq(user_id,job_id,comments)
            if status == 2:
                direct_mail_sent(email,trail)
                return "You will receive your report soon.."
            elif status == 0 or status==1:
                return "file is under procesing"
        else:
            job_id=enterMalware(filename,user_id)
            setReq(user_id,job_id,comments)
            
            files.seek(0) #getting the file pointer to the start 
        
            files.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            #print("hi")
           # with ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as myzip:
            #  myzip.write(filename)
            #print("zipped")
            # changing file permissions 
            os.chmod(os.path.join(app.config['UPLOAD_FOLDER'],filename),0o777)
           
            #cursor.execute("insert into omr_data values (DEFAULT,%s,%s,%s,NULL,'pending')",(email,filename,comments))
            
            #cursor.execute("select job_id from omr_data where file_hash=%s AND job_status='pending';",(filename,))
            #job_id=list(cursor.fetchall()[0])[0] 
            
            pushqueue(file_md5_hash, job_id)
            # file_md5_hash=""
            files.seek(0)
            #update_email_list(cursor, filename, email)
            #flash("File Submitted Successfully!")
            return render_template("filesuccess.html")
            
            
   
@app.route('/upload_file/', methods=['POST'])
def upload_file():
        file = request.files['file']

if __name__=="__main__":
    # db.create_all()
    app.debug=False
    #app.run(host='10.21.238.198', port
    app.run(host='127.0.0.1', port='5000')
    #app.run()
    
