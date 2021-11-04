from typing import Text
from flask import Blueprint, render_template, request
import sys

#Create Blueprint
rooms = Blueprint('rooms', __name__)

@rooms.route('/addRoom', methods=['GET', 'POST'])
def addRoom():
    if request.method == "POST":
        featureList_2 = request.form["featureList"]
        print("COPY THAT")
        print(featureList_2)
    else:
        print("==================>>>>>>>>>>========================>", file=sys.stderr)
    print("HERE_SSS")
    return render_template("addReview.html")

@rooms.route('/viewRoom', methods=['GET', 'POST'])


def viewRoom():
    #The backend (.db file) will pass the following things to room.html, so it can be displayed in the frontend
    #Featured Picture, Feature #1, Feature #2, Feature #3, Overall Rating, List of all the Reviews, Pictures (Only 3 will be displayed)

    #pictures[0] = Main "Featured" Picture, pictures[1] = Bottom Picture_1, pictures[2] = Bottom Picture_2, pictures[3] = Bottom Picture_3
    #pictures = ["will", "it", "work"]
    #features = ["I hope it", "does"]
    #overallRating = 5
    #lReviews = []
 
    return render_template("room.html")