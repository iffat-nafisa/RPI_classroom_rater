from typing import Text
from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Room

#Create Blueprint
rooms = Blueprint('rooms', __name__)

# @rooms.route('/addRoom', methods=['GET', 'POST'])
# def addRoom():
#     print("Hi")
#     #uses the name
#     if request.method == "POST":
#         user = request.form['nm']
#         if (user == "work"):
#             return render_template("index.html")
#         else:
#             return render_template("room.html")
        

#     print("hereeeee")
#     return render_template("addReview.html")

# @rooms.route('/addRoom', methods=['GET', 'POST'])
# def addRoom():
#     if request.method == "POST":
#         building = request.form.get("building")
#         room_no = request.form.get("room")
#         room_exists = db.session.query(Room.number).filter_by(number=room_no).count()
#         if room_exists > 0:
#             return redirect(url_for('rooms.viewRoom'))
#         room = Room(number=room_no, building_name=building)
#         db.session.add(room)
#         db.session.commit()
#         return redirect(url_for('rooms.viewRoom'))
       
#     return render_template("index.html")


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