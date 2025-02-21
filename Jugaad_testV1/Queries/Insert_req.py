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

def setReq(user_id , job_id, comment):
	query = "insert into request_table (user_id , job_id,comment)values(%s , %s , %s)"
	cursor.execute(query,(user_id,job_id,comment))
	result = cursor.fetchone()
	if result:
		return 1
	else:
		return 0
print(setReq(1727932818126,2,"ae hallo"))
