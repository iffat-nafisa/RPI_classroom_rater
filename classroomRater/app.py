from flask import Flask, g, render_template, redirect, url_for, request, abort
from flask_login import LoginManager
from os import path
from peewee import SqliteDatabase
from models import db, DB_NAME, addSchoolAndBuildings
from flask_sqlalchemy import SQLAlchemy
from views import views
from werkzeug.utils import secure_filename
import os
import imghdr
import uuid

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

# Set up flask and database; Initiate the web application
app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = '/uploads'
db.init_app(app)
app.register_blueprint(views, url_prefix='/')

# Create temporary database
# @param app the current running application
def create_database(app):
    if not path.exists(DB_NAME):
        db.create_all(app=app)
        print('Created Database!')


# Store image file in uploads
# if valid, return true
# else return false 
# def upload_files(uploaded_file):
#     filename = secure_filename(uploaded_file.filename)
#     if filename != '':
#         file_ext = os.path.splitext(filename)[1]
#         if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
#                 file_ext != validate_image(uploaded_file.stream):
#             return [False, ""]
#         image_id = str(uuid.uuid4)
#         file_name = image_id + '.png'
#         uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], file_name))
#     return [True, image_id]

# Main method for initiating the app
#Create temporary database, then run app
if __name__ == '__main__':
    create_database(app)
    app.run(debug=DEBUG, host=HOST, port=PORT)
    
