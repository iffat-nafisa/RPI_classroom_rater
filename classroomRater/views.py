from flask import Blueprint, render_template, request, redirect, url_for,flash
from models import db, Room, addSchoolAndBuildings, Review, Feature
import time

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


def ave(reviews):
    con=0
    s=0
    for r in reviews:
        if r.rating != -1:
            con=con+1
            s=s+r.rating
    if con == 0:
        return 0
    return s/con





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
    room=Room(number=roomName, building_name=buildingName)
    room=room.query.filter_by(number=roomName, building_name=buildingName).first()
    featureList = room.features
    reviewList =room.reviews
    avgRating = ave(reviewList)
    
    # change the line above to take from database
    frequency = {}
    for item in featureList:
        # checking the element in dictionary
        if item in frequency:
            # incrementing the counr
            frequency[item] += 1
        else:
            # initializing the count
            frequency[item] = 1

    frequency = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
    lst = []
    for f in frequency:
        lst.append(f)
    allFeatures=[]
    if(len(lst)<3):
        for i in range(0,3):
            if(i>=len(lst)):
                allFeatures.append('Empty')
            else:
                print(lst)
                print(lst[i])
                allFeatures.append(lst[i][0])
    else:
        
        allFeatures =[lst[0][0], lst[1][0],lst[2][0]]

    userShowReview = reviewList
    current_building = buildingName
    current_room = roomName

    if request.method == "POST": # this needs to render the createReview page - addReview.html using the correct building name and room name
        return redirect(url_for('views.createReview',buildingName=buildingName, roomName=roomName))

    
    
    # allReviews=[]
    # allPictures=[]

    #**locals() passes all the local variables defines in this function to room.html
    return render_template("room.html", **locals())



def checkStars():
    x = 5
    while x > 0:
        stars = request.form.get("star"+str(x))
        if stars == "1":
            return 6-x
        x -= 1
    return -1


@views.route('/createReview/<buildingName>/<roomName>', methods=['GET', 'POST'])
def createReview(buildingName, roomName):
    print("Before createReview", request.method)
    if request.method == "POST":
        request.method = "GET"
        # send review to database 
        review = request.form.get("reviewTextbox")
        if review == "" or review == None:
            review = " "

        featureList = request.form.get("featureList")
        rating = checkStars()
        print(round(rating, 1))

        review_o = Review(id = hash(time.time()), rating=rating, written_review=review, room_number=roomName, building_name=buildingName)
        features = featureList.split(";")
        featuresUpdated = []
        room = db.session.query(Room.number, Room.building_name).filter_by(number=roomName, building_name=buildingName).first()
        print(room)
        for f in features:
            f = f.strip()
            f = f.title()
            featuresUpdated.append(f)
            f_o = Feature(id=hash(time.time()), description=f, room_number=roomName, building_name=buildingName)
            db.session.add(f_o)
            db.session.commit()

        review_o = Review(id = hash(time.time()), rating=5, written_review=review, room_number=roomName, building_name=buildingName)
        db.session.add(review_o) # add to the database 
        db.session.commit()
        return redirect(url_for('views.viewRoom',buildingName=buildingName, roomName=roomName))

    return render_template("addReview.html")
