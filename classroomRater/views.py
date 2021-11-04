from flask import Blueprint, render_template, request

#Create Blueprint
views = Blueprint('views', __name__)

#This function will run whenever go to the "/" root
@views.route('/', methods=['GET', 'POST'])
def homepage():
    return render_template("index.html")