import os 
import uuid
import pika 
import hashlib
import json
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message


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
app.config['UPLOAD_FOLDER']='/home/omrapp/lol/File_hash/'


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
mail=Mail(app)
db= SQLAlchemy(app)

# class users(db.Model):
#      _id = db.Column("ID", db.Integer, primary_key=True)
#      email_id=db.Column(db.String(100))
#      file_uuid=db.Column(db.String(100))
#      request_count=db.Column(db.Integer)

#      def __init__(self, email_id, file_uuid, request_count):
          
#           self.email_id=email_id
#           self.file_uuid=file_uuid
#           self.request_count=request_count


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
        
        #print(files, email, comments)
        
     #   msg= Message('JUGAAD Testbed - Your runtime trails are ready !', sender='allan.n.pais@gmail.com', recipients=[request.form['email']])
      #  msg.body='Dear '+email+'Your runtime trails are available in the file below. \n Thank you for using OpenMalwareResearch!'
# /home/allan/Desktop/OMR_CB/Jugaad_test/instance/test.txt'
       # with app.open_resource("/home/allan/Desktop/OMR_CB/Jugaad_test/instance/received_files/test.txt") as fp:
        #with app.open_resource(os.path.join(app.instance_path, 'test.txt')) as fp:
        # msg.attach("test.txt", "application/txt", fp.read())
        #mail.send(msg)

        #filename="["+str(uuid.uuid4())+"]_"+files.filename
        #bytestring=str.encode(secure_filename(files.filename))
        filename=secure_filename(files.filename)
        
       # file_md5_hash=hashlib.md5(files.read()).hexdigest()
        #filename=file_md5_hash
        #put the file in the database and then query the jobid number 
        
        #sample data 
        job_id=1001
        #sample data 
        
        
        print(email)
        #os.makedirs(os.path.join(app.instance_path, 'Uploaded_files'))
        file_md5_hash=hashlib.md5(files.read()).hexdigest()
        filename=file_md5_hash
        files.seek(0) #getting the file pointer to the start 
        files.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        os.chmod(os.path.join(app.config['UPLOAD_FOLDER'],filename),0o666)
        
        print(file_md5_hash)
        #os.rename(os.path.join(app.config['UPLOAD_FOLDER'],filename),os.path.join(app.config['UPLOAD_FOLDER'],file_md5_hash)) 
        pushqueue(file_md5_hash, job_id)
        file_md5_hash=""
        return "File pushed to the message queue successfully! Press back to continue"
    
 
@app.route('/upload_file/', methods=['POST'])
def upload_file():
        file = request.files['file']
if __name__=="__main__":
    # db.create_all()
    
    app.debug=True
    app.run()
