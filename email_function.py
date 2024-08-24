import pika 
import json 
from flask import Flask
from flask_mail import Mail, Message

from flask_cors import CORS
app = Flask(__name__)


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

def SendEmail(ch, method, properties, body):
    
    json_value=json.loads(body)
    print("Loaded json value")
    fileuuid=json_value["File_uuid"]
    job_id=json_value["Jobid"]
    
    email="21f1001663@ds.study.iitm.ac.in"
    msg= Message('JUGAAD Testbed - Your runtime trails are ready !', sender='allan.n.pais@gmail.com',recipients=email)
    msg.body='Dear '+email+'Your runtime trails are available in the file below. \n Thank you for using OpenMalwareResearch!'
    with app.open_resource(f'/home/omrapp/Desktop/Jugaad_test/script.js') as fp:
        #with app.open_resource(os.path.join(app.instance_path, 'test.txt')) as fp:
      msg.attach("script.js", "application/txt", fp.read())   
      mail.send(msg)
    print("Job processed from queue and email sent to the user")
    print("Job Closed Successfully")
@app.route("/")

def send():
    credentials = pika.PlainCredentials('OMR_RMQ','Omr@123')
    connection = pika.BlockingConnection(pika.ConnectionParameters('172.23.254.74', 5672, '/', credentials))
    channel=connection.channel()
    channel.queue_declare("queue_2")
    channel.basic_consume(queue="queue_2", auto_ack=True, on_message_callback=SendEmail)
    return "ok"
    

  


if __name__=="__main__":
    # db.create_all()
    
    app.debug=True 

    app.run(host='localhost',port=5001)
