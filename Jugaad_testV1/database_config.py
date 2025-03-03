from app_config import *
def update_email_list(cursor, file_hash, email):
    query_elist = """
    UPDATE omr_data
    SET email_list = array_append(email_list, %s)
    WHERE file_hash = %s;
    """
    cursor.execute(query_elist, (email, file_hash))
#--------------------------------------------------
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
    cursor.execute(query, (email,))  # Execute the query
    count = cursor.fetchone()[0]     # Fetch the result
    print("Count:", count)
   
    if count >= 2:     # Check the count and return the appropriate message
        print("Your two files are already under processing/pending, kindly wait till they get processed and submit it later.")
        return 1;
    else:
        return 0;

#--------------------------------------------------
def pushqueue(filehash, jobid):
  
  credentials = pika.PlainCredentials('OMR_RMQ', 'Omr@123')
  connection = pika.BlockingConnection(pika.ConnectionParameters('172.23.254.74', 5672, '/',   credentials))

  channel =connection.channel()

  channel.queue_declare("queue_1")
  
  message = { 'File_Hash':filehash,
               'Job_Id':jobid }
  
  channel.basic_publish(exchange='',
                      routing_key='queue_1',
                      body=json.dumps(message) )

  print("Message pushed to the queue")
#---------------------------------Newly Designed Function ----------------------------------------------------------------------

def User_Check(email):
    query_check = "SELECT User_Id, NOR FROM User_Table WHERE Email = %s;" # Check if the user already exists in the User_Table
    cursor.execute(query_check, (email,))
    result = cursor.fetchone()

    if result:  # User exists, extract User_Id and current NOR
        user_id = result[0]  
        current_nor = result[1]
        new_nor = current_nor + 1   # Increment NOR (Number of Requests)
        query_update_nor = "UPDATE User_Table SET NOR = %s WHERE User_Id = %s;"
        cursor.execute(query_update_nor, (new_nor, user_id))
        return user_id   # Return the existing User_Id
    
    else:       # User does not exist, insert new user with unique User_Id based on reduced timestamp
        
        current_time = int(time.time() * 1000)  # Use milliseconds since epoch, fits within BIGINT
        # Insert new user into the User_Table
        query_insert = """   
        INSERT INTO User_Table (User_Id, Email, Date, NOR)
        VALUES (%s, %s, CURRENT_TIMESTAMP, 1);  -- New user, so NOR starts at 1
        """
        cursor.execute(query_insert, (current_time, email))
        return current_time  # Return the newly generated User_Id

#--------------------------------------------------
def checkMalware(filehash):
    query = "select * from malware_table where filehash = %s"
    cursor.execute(query,(filehash,))
    result = cursor.fetchone()
    if result:#--------------------------------------------------
        jobId = result[0]
        trail = result[2]
        status= result[4]
        return  status,trail,jobId
    else:
        return -1,-1,-1
        
#--------------------------------------------------
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
#--------------------------------------------------
def setReq(user_id , job_id, comment):
    query = "insert into request_table (user_id , job_id,comment)values(%s , %s , %s)"
    cursor.execute(query,(user_id,job_id,comment))
    result = cursor.fetchone
    if result:
        return 1
    else:
        return 0