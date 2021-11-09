from flask import Blueprint, render_template, request, redirect, url_for,flash
from models import db, Room, addSchoolAndBuildings


#Create Blueprint
views = Blueprint('views', __name__)

# this is the master building list that contains all RPI acidemic building
buildingList = ["DCC", "SAGE", "Amos Eaton Hall", "Carnegie Building", "Center for Biotechnology and Interdisciplinary Studies", "CBIS", "Chapel + Cultural Center", "Experimental Media and Performing Arts Center", "EMPAC", "Folsom Library", "Greene Building","Gurley Building", "Hirsch Observatory", "Houston Field House", "Jonsson Engineering Center", "Low Center", "West Hall", "Winslow Building"]


# this function will show the user an error message in red.
def errorMessage(message):
    flash(message,category='error')
    pass



# this funciton will check to make sure that the text in the building search bar 
# is included in one of the buildings in the master building list
def checkBuildingInput(building):
    for b in buildingList: # loop through all the master building list 
        if building.lower() in b.lower():
            building = b
            return building
    return None


# this function will check to make sure that the text in the room search bar is an integer.
def checkRoomInput(room):
    try:
        int(room)
        return True
    except ValueError:
        return False





#This function will run whenever go to the "/" root
@views.route('/', methods=['GET', 'POST'])
def homepage():
    addSchoolAndBuildings()
    if request.method == "POST":
        building = request.form.get("building")

        if building == None or building == "":
            errorMessage("Please type input")
            return render_template("index.html")

        building = checkBuildingInput(building)


        if building == None:
            errorMessage('Building must be a valid RPI building.')

            return render_template("index.html")

        room_no = request.form.get("room")
        if room_no == None or room_no == "":
            errorMessage("Please type input")
            return render_template("index.html")

        if not checkRoomInput(room_no): # check that the room is an integer number
            errorMessage('Room number must be a number.')
            return render_template("index.html")

        room_exists = db.session.query(Room.number).filter_by(number=room_no).count()
        if room_exists > 0:
            return redirect(url_for('views.viewRoom',buildingName=building, roomName=room_no))

        room = Room(number=room_no, building_name=building)
        db.session.add(room) # add to the database 
        db.session.commit()
        return redirect(url_for('views.createReview', buildingName=building,roomName=room_no)) # redirect the user to that room page


    return render_template("index.html")    



@views.route('/viewRoom/<buildingName>/<roomName>', methods=['GET', 'POST'])
def viewRoom(buildingName, roomName):
    # The backend (.db file) will pass the following things to room.html, so it can be displayed in the frontend
    # Featured Picture, Feature #1, Feature #2, Feature #3, Overall Rating, List of all the Reviews, Pictures (Only 3 will be displayed)

    # note: The first three elements of the list are considered to be the "featured" features shown in the room.html
    allFeatures =["No AC", "Less Space", "Has projector"]
    avgRating = 5
    current_building = buildingName
    current_room = roomName
    
    # allReviews=[]
    # allPictures=[]

    #**locals() passes all the local variables defines in this function to room.html
    return render_template("room.html", **locals())





@views.route('/createReview/<buildingName>/<roomName>', methods=['GET', 'POST'])
def createReview(buildingName, roomName):

    if request.method == "POST":
        print("here")
        return viewRoom(buildingName, roomName)


    return render_template("addReview.html")
