from email_config import *
from database_config import *

username_list=[]

#-------------------------------------------------- Flask controllers are stated below 
@app.route("/")
def welcome():
    
    #return render_template("index.html")
    return redirect(url_for('login_google'))
#--------------------------------------------------
@app.route("/login/google")
def login_google():
    try:
    
        redirect_uri=url_for('authorize_google', _external=True)
        return google.authorize_redirect(redirect_uri)
    
    except Exception as e:
         
         print("There was an error in the google authentication")
         return f"Error occoured during login {str(e)}", 500
#--------------------------------------------------
@app.route("/authorize/google")    #app.run()
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
     session["oauth_token"]=token['access_token']

     print("From the authorize function call usename is ", session['username'])
     print("From the authorization function call token is", session['oauth_token'])
     
     return redirect(url_for('send_upload'))
#--------------------------------------------------
@app.route('/fileupload', methods = ['GET'])
def send_upload():
    
    return render_template("index.html")
#--------------------------------------------------
@app.route('/filesend', methods = ['POST'])
def receive():

    print("The value of the path is  ",app.instance_path)
    if request.method == 'POST':

        try:    #app.run()
            files = request.files['files']
        except KeyError:
            return "Missing 'name' key in the form!"
    
        email = request.form['email'] 
        user_id = User_Check(email) #now here we will check whether the us•••••••er exist here or not 
        comments = request.form['comments']    #app.run()
        filename=secure_filename(files.filename)
        file_md5_hash=filename 
        file_md5_hash=hashlib.md5(files.read()).hexdigest()
        filename=file_md5_hash+".dat" 
       
        #now here we have to check the status of the malware 
        status,trail,job_id = checkMalware(filename)
        
        if status !=-1 and trail!=-1 and job_id!=-1:
            setReq(user_id,job_id,comments)
            if status == 2:    #app.run()
                direct_mail_sent(email,trail)
                return "You will receive your report soon.."
            elif status == 0 or status==1:
                return "file is under procesing"
        else:    #app.run()
            job_id=enterMalware(filename,user_id)
            setReq(user_id,job_id,comments)
            
            files.seek(0) #getting the file pointer to the start fileupload
            #app.run()# Insert new user into the User_Table
            files.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
         
            os.chmod(os.path.join(app.config['UPLOAD_FOLDER'],filename),0o777)
       
            pushqueue(file_md5_hash, job_id)
            files.seek(0)
            #username=session['username']
            #print("The Oauth token is", username)
            #print("The type of the oauth token is", type(username))
            #subprocess.Popen(f'curl -X POST "https://accounts.google.com/o/oauth2/revoke" -d {token}', shell=True)
            
            #requests.post(f"http://omr.iitm.ac.in/oauth/v2/{token["access_token"]}/revoke")
            session.clear()
            # client_id.auth.revoke_token()
            
            return render_template("filesuccess.html")
#--------------------------------------------------
# @app.route('/upload_file/', methods=['POST'])
# def upload_file():
#         file = request.files['file']