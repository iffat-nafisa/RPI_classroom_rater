from typing import Text
from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Room

#Create Blueprint
rooms = Blueprint('rooms', __name__)



# this is the master building list that contains all RPI acidemic building





# this function will search a room in a building that the user puts into the search bar. 
# If the room does not exist it will add the room.
# If the user inputs invalid text into either of the search bars then they will get 
# an error message. 
@rooms.route('/addRoom', methods=['GET', 'POST'])
def addRoom():
    if request.method == "POST":
        building = request.form.get("building")
        
        if not checkBuildingInput(building):
            errorMessage("Building must be a valid RPI building.")
            return render_template("index.html")

        room_no = request.form.get("room")

        if not checkRoomInput(room_no): # check that the room is an integer number
            errorMessage("Room number must be a number.")
            return render_template("index.html")

        room_exists = db.session.query(Room.number).filter_by(number=room_no)
        if room_exists:
            return redirect(url_for('rooms.createReview'))

        room = Room(number=room_no, building_name=building)


        # TODO this needs to be changed to the above. But "room in database" isnt the right way to do that
        db.session.add(room) # add to the database 
        db.session.commit()
        return redirect(url_for('rooms.viewRoom')) # redirect the user to that room page


        
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

@rooms.route('/createReview', methods=['GET', 'POST'])
def createReview():
    return render_template("addReview.html")
