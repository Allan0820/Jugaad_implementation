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


print(User_Check("Abcde@gmail.com"))


