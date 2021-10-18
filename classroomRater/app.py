from flask import Flask, g, render_template, redirect, url_for, request
from flask_login import LoginManager
import sqlite3
from peewee import SqliteDatabase
import models

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = "secret"

login_manager = LoginManager()


@app.route('/')
def homepage():
    return render_template("index.html")


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response


if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, host=HOST, port=PORT)
