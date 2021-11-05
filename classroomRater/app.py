from flask import Flask, g, render_template, redirect, url_for, request
from flask_login import LoginManager
from os import path
from peewee import SqliteDatabase
from models import db, DB_NAME
from flask_sqlalchemy import SQLAlchemy
from views import views
from rooms import rooms

def create_database(app):
    if not path.exists(DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.config['secret_key'] = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db.init_app(app)
create_database(app)
app.register_blueprint(views, url_prefix='/')
app.register_blueprint(rooms, url_prefix='/')


if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)

