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
def getEmail(user_ids):
    # Create placeholders for each user_id in the tuple
    placeholders = ', '.join(['%s'] * len(user_ids))
    query = f"SELECT email FROM user_table WHERE user_id IN ({placeholders})"
    
    # Execute the query with the tuple of user_ids
    cursor.execute(query, user_ids)  # user_ids is already a tuple
    result = cursor.fetchall()  # Fetch all matching rows

    if result:
        # Extract emails from the result tuples
        emails = [row[0] for row in result]  # row[0] gets the email from each tuple
        return emails
    else:
        return [""]  # Return an empty string if no results are found

# Example call with a tuple
print(getEmail((21, 22)))

	
