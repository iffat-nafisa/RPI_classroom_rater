from flask import Flask, g, render_template, redirect, url_for, request
from flask_login import LoginManager
from os import path
from peewee import SqliteDatabase
from models import db, DB_NAME, addSchoolAndBuildings
from flask_sqlalchemy import SQLAlchemy
from views import views
from rooms import rooms



DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db.init_app(app)

app.register_blueprint(views, url_prefix='/')
app.register_blueprint(rooms, url_prefix='/')


def create_database(app):
    if not path.exists(DB_NAME):
        db.create_all(app=app)
        print('Created Database!')


if __name__ == '__main__':
    create_database(app)
    app.run(debug=DEBUG, host=HOST, port=PORT)
    
