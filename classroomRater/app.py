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


# @app.route('/register', methods=('GET', 'POST'))
# def register():
#     form = forms.RegisterForm()
#     if form.validate_on_submit():
#         flash("Yay, you registered!", "success")
#         teacher_b = True if form.category.data == "teacher" else False
#         parent_b = True if form.category.data == "parent" else False
#         student_b = True if form.category.data == "student" else False
#         models.User.create_user(
#             username=form.username.data,
#             email=form.email.data,
#             password=form.password.data,
#             teacher=teacher_b,
#             parent=parent_b,
#             student=student_b
#         )
#         return redirect(url_for('login'))
#     return render_template('register.html', form=form)

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, host=HOST, port=PORT)
