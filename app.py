# https://roytuts.com/upload-and-display-image-using-python-flask/
from flask import Flask

UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)
app.secret_key = '1234'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024