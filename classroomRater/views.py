from flask import Blueprint, Flask, render_template

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def homepage():
    return render_template("index.html")
