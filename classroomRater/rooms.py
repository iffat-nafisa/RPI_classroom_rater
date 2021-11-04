from typing import Text
from flask import Blueprint, render_template, request
import sys

#Create Blueprint
rooms = Blueprint('rooms', __name__)

@rooms.route('/addRoom', methods=['GET', 'POST'])
def addRoom():
    #uses the name
    if request.method == 'post':
        user = request.form['nm']
        print("This is the user's value", user)

    print("hereeeee")
    return render_template("addReview.html")



@rooms.route('/viewRoom', methods=['GET', 'POST'])


def viewRoom():
    #The backend (.db file) will pass the following things to room.html, so it can be displayed in the frontend
    #Featured Picture, Feature #1, Feature #2, Feature #3, Overall Rating, List of all the Reviews, Pictures (Only 3 will be displayed)

    #note: The first three elements of the list are considered to be the "featured" features shown in the room.html
    allFeatures =["No AC", "Less Space", "Has projector"]
    avgRating = 5
    
    #allReviews=[]
    #allPictures=[]

    #**locals() passes all the local variables defines in this function to room.html
    return render_template("room.html", **locals())