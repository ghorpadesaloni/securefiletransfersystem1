from flask import Flask, render_template, session, redirect, url_for, request
from flask_session import Session
from user import register, login, logout
from werkzeug.utils import secure_filename
import os

# Create a Flask app instance
app = Flask(__name__)

# Set a secret key to secure the session
app.secret_key = 'my_super_secret_key'  # Replace with your actual secret key

# Use Flask-Session to handle the session (note: this is a client-side session, not recommended for production)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Configure the database URI for PostgreSQL
# Replace 'ruegen', 'ruegen', and 'postgres-container' with appropriate values
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://ruegen:ruegen@postgres-container/secure_file_system"

# Register routes from the 'user' module
app.add_url_rule('/register', view_func=register, methods=['GET', 'POST'])
app.add_url_rule('/login', view_func=login, methods=['GET', 'POST'])
app.add_url_rule('/logout', view_func=logout)

# Define a route for the dashboard page (set it as the default route)
@app.route('/')
def default():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

# Define a route for the dashboard page
@app.route('/dashboard')
def dashboard():
    # Check if the user is logged in
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Render the dashboard template
    return render_template('dashboard.html', username=session['username'])

# Define a route for the combined upload/file-upload page
@app.route('/manage-files', methods=['GET', 'POST'])
def upload_file():
    # Check if the user is logged in
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            # Secure the filename and save the file
            filename = secure_filename(uploaded_file.filename)
            file_path = os.path.join('uploads', filename)
            uploaded_file.save(file_path)
            
            # Handle file storage logic here
            
            # Redirect to the dashboard or another appropriate page
            return redirect(url_for('upload'))
    
    # Retrieve user-specific file information (replace with actual logic)
    my_files = [
        {'filename': 'file1.txt', 'filesize': '100 KB', 'upload_date': '2023-08-20', 'file_link': '#'},
        {'filename': 'file2.pdf', 'filesize': '1.2 MB', 'upload_date': '2023-08-21', 'file_link': '#'},
        # Add more file entries as needed
    ]
    
    # Render the combined upload/file-upload template and pass the file information
    return render_template('manage-files.html', username=session['username'], my_files=my_files)

# Define a route for the send files page
@app.route('/send-files')
def send_files():
    # Check if the user is logged in
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Render the send-files template
    return render_template('send_files.html', username=session['username'])

# ... Implement email sending logic here ...

if __name__ == '__main__':
    app.run(debug=True)
