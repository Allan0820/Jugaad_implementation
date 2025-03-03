from imports import *
from apikey import *
app = Flask(__name__)
app.config["SESSION_PERMANENT"]=False
app.config["PERMANENT_SESSION_LIFETIME"]=timedelta(seconds=10)
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
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
app.config['MAIL_USERNAME']='allan.n.pais@gmail.com'
app.config['MAIL_SENDER']='allan.n.pais@gmail.com'
app.config['MAIL_PASSWORD']='fgyy axcd depv vexe'
app.config['MAIL_DEFAULT_SENDER']=None
app.config['MAIL_MAX_EMAILS']=None
app.config['MAIL_ASCII_ATTACHMENTS']=False
app.config['SECRET_KEY']=SECRET_KEY


oauth=OAuth(app)
google = oauth.register(
     name='google',
     client_id=CLIENT_ID,
     client_secret=CLIENT_SECRET,
     server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
     client_kwargs={'scope':'openid profile email'},
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
credentials=pika.PlainCredentials('OMR_RMQ','Omr@123')
connection2 = pika.BlockingConnection(pika.ConnectionParameters('172.23.254.74', 5672,'/', credentials))