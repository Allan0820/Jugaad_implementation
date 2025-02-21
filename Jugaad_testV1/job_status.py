import psycopg2
from flask import Flask, render_template, request

# Initialize Flask application
app = Flask(__name__)

# Configure the Flask application
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # Max upload size: 100MB
app.config['UPLOAD_FOLDER'] = '/home/omrapp/Desktop/filehash/'  # Upload folder path

# Configure database connection
connection = psycopg2.connect(
    database="omrdatabase",
    host="172.23.254.74",
    port=5432,
    user="omruser",
    password="Omr@123"
)
cursor = connection.cursor()
connection.autocommit = True

@app.route('/', methods=['GET', 'POST'])
def index():
    job_status = None
    
    if request.method == 'POST':
        job_id = request.form.get('job_id')
        
        cur = connection.cursor()
        
        # Query to get job status
        cur.execute('SELECT job_status FROM omr_data WHERE job_id = %s', (job_id,))
        result = cur.fetchone()
        
        cur.close()
        
        if result:
            job_status = result[0]
        else:
            job_status = 'Job ID not found'
    
    return render_template('status.html', job_status=job_status)

@app.route('/upload_file/', methods=['POST'])
def upload_file():
    file = request.files['file']
    # Add file processing code here

if __name__ == "__main__":
    app.run(debug=True)

