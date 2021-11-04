from flask import Blueprint

#Create Blueprint
rooms = Blueprint('rooms', __name__)

@rooms.route('/addRoom', methods=['GET', 'POST'])
def addRoom():
    return "<h1> Testing addReview </h1>"

@rooms.route('/viewRoom', methods=['GET', 'POST'])
def viewRoom():
    return "<h1> Testing viewRoom </h1>"