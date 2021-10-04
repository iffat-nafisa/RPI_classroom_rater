from flask import (Flask, render_template )
from flask_login import LoginManager

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
# app.secret_key = ''

login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'

@app.route('/')
def homepage():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)