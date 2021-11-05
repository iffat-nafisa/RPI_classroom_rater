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

buildingList = ["DCC", "SAGE", "Amos Eaton Hall", "Carnegie Building", "Center for Biotechnology and Interdisciplinary Studies", "CBIS", "Chapel + Cultural Center", "Experimental Media and Performing Arts Center", "EMPAC", "Folsom Library", "Greene Building","Gurley Building", "Hirsch Observatory", "Houston Field House", "Jonsson Engineering Center", "Low Center", "West Hall", "Winslow Building"]

def errorMessage(message):
    # make flash that prints the error onto HTML in red
    pass


@rooms.route('/addRoom', methods=['GET', 'POST'])
def addRoom():
    if request.method == "POST":
        building = request.form.get("building")
        go = False
        for b in buildingList:
            if building.lower() in b.lower():
                go = True
                building = b
                break
        if not go:
            errorMessage("Building must be a valid RPI building.")
            return

        room_no = request.form.get("room")
        try:
            int(room_no)
        except ValueError:
            errorMessage("Room number must be a number.") 
            return
        
        room_exists = db.session.query(Room.number).filter_by(number=room_no)
        if room_exists:
            return redirect(url_for('rooms.viewRoom'))
        room = Room(number=room_no, building_name=building)
        db.session.add(room)
        db.session.commit()
        return redirect(url_for('rooms.viewRoom'))

        
    return render_template("index.html")


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