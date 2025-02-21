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


import smtplib
import smtplib


connection = psycopg2.connect(
                      database="omrdatabase", 
                      host="172.23.254.74", 
                      port=5432,
                      user="omruser",
                      password="Omr@123" ,
                    )

cursor=connection.cursor()
connection.autocommit=True


import datetime

import datetime
import time


def checkMalware(filehash):
	query = "select * from malware_table where filehash = %s"
	cursor.execute(query,(filehash,))
	result = cursor.fetchone()
	if result:
		jobId = result[0]
		trail = result[2]
		status= result[4]
		return  status,trail
	else:
		return -1,-1
		
	
	
status,th = checkMalware('aa')
print(status)
print(th)
			


 

