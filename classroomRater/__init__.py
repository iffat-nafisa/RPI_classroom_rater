from flask import Flask
from flask_login import LoginManager
from os import path
import sqlite3
from flask_sqlalchemy import SQLAlchemy

#db = SQLAlchemy()
#DB_NAME = 'classroomrater.db'

#DEBUG = True
#PORT = 8000
#HOST = '0.0.0.0'

def create_app():
    app = Flask(__name__)
    app.config['secret_key'] = "secret"
    #app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    #db.init_app(app)

    #Import the blueprints: .[fileName] [blueprintName]
    from .views import views
    from .rooms import rooms
    
    #Register all the blueprints created
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(rooms, url_prefix='/')

    return app


#def create_database(app):
#    if not path.exists(DB_NAME):
#        db.create_all(app=app)
#        print('Created Database!')
    

# login_manager = LoginManager()


# @app.before_request
# def before_request():
#     """Connect to the database before each request."""
#     g.db = models.DATABASE
#     g.db.connect()


# @app.after_request
# def after_request(response):
#     """Close the database connection after each request."""
#     g.db.close()
#     return response


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


