#!/home/omrapp/Desktop/Jugaad_testV1/bin/python


from apikey import *
from imports import *
from database_config import *
from controller_config import *
from email_config import *
from app_config import *


if __name__=="__main__":
    app.debug=False
    
    app.run(host='127.0.0.1', port='5000')
    
