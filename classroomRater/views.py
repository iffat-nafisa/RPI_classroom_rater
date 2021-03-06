from flask import Flask, Blueprint, config, render_template, request, redirect, url_for,flash, abort
from models import db, Room, addSchoolAndBuildings, Review, Feature, Img
import time
from werkzeug.utils import secure_filename
import os
import imghdr
import uuid

#Create Blueprint
views = Blueprint('views', __name__)
extensions = ['jpg', 'png', 'gif']
imagePath = 'static/'
# this is the master building list that contains all RPI acidemic building
buildingList = ["DCC", "SAGE", "Amos Eaton Hall", "Carnegie Building", "Center for Biotechnology and Interdisciplinary Studies", "CBIS", "Chapel + Cultural Center", "Experimental Media and Performing Arts Center", "EMPAC", "Folsom Library", "Greene Building","Gurley Building", "Hirsch Observatory", "Houston Field House", "Jonsson Engineering Center", "Low Center", "West Hall", "Winslow Building"]
# this function will show the user an error message in red.
def errorMessage(message):
    flash(message,category='error')


# Validate the input image 
def validate_image(filename):
    if '.' in filename:
        if filename.rsplit('.', 1)[1].lower() in extensions:
            return True
    return False


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


# this function will get the average rating for a room using only the valid ratings
# invalid ratings are ones that are -1.
# will return 5 if there are no ratings
def ave(reviews):
    total=0
    s=0
    for r in reviews:
        if r.rating != -1:
            total=total+1
            s=s+r.rating
    if total == 0:
        return 5
    return s/total





#This function will run whenever go to the "/" root
@views.route('/', methods=['GET', 'POST'])
def homepage():
    addSchoolAndBuildings()
    if request.method == "POST":
        building = request.form.get("building")

        if building == None or building == "":
            errorMessage("Please type input")
            # rerender the page because their input was invalid
            return render_template("index.html")

        building = checkBuildingInput(building)


        if building == None:
            errorMessage('Building must be a valid RPI building.')
            # rerender the page because their input was invalid
            return render_template("index.html")

        room_no = request.form.get("room")
        if room_no == None or room_no == "":
            errorMessage("Please type input")
            # rerender the page because their input was invalid
            return render_template("index.html")

        if not checkRoomInput(room_no): # check that the room is an integer number
            errorMessage('Room number must be a number.')
            return render_template("index.html")

        room_number_exists = db.session.query(Room.number).filter_by(number=room_no).count()
        room_building_exists = db.session.query(Room.building_name).filter_by(building_name=building).count()
        if (room_number_exists > 0 )&( room_building_exists>0 ):
            # redirect to the view room page because this room was found in the database
            return redirect(url_for('views.viewRoom',buildingName=building, roomName=room_no))

        room = Room(number=room_no, building_name=building)
        db.session.add(room) # add to the database 
        db.session.commit()
        # redirect to create review page because this review was not found in the database 
        return redirect(url_for('views.createReview', buildingName=building,roomName=room_no)) # redirect the user to that room page


    return render_template("index.html")    



# this is the python part of the view room HTML code
@views.route('/viewRoom/<buildingName>/<roomName>', methods=['GET', 'POST'])
def viewRoom(buildingName, roomName):
    # The backend (.db file) will pass the following things to room.html, so it can be displayed in the frontend
    # Featured Picture, Feature #1, Feature #2, Feature #3, Overall Rating, List of all the Reviews, Pictures (Only 3 will be displayed)

    # note: The first three elements of the list are considered to be the "featured" features shown in the room.html
    room=Room(number=roomName, building_name=buildingName)
    room=room.query.filter_by(number=roomName, building_name=buildingName).first()
    if room != None:
        featureList = room.features
        reviewList =room.reviews
    else:
        featureList = []
        reviewList = []
    
    avgRating = round(ave(reviewList),1)
    
    # change the line above to take from database
    frequency = {}
    for item in featureList:
        # checking the element in dictionary
        if item.description.upper() in frequency:
            # incrementing the counr
            frequency[item.description.upper()] += 1
        else:
            # initializing the count
            frequency[item.description.upper()] = 1

    # sort the features by the number of occurances
    lst = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
    allFeatures=[]
    if(len(lst)<3): # if there are less than 3 reviews only display the ones we have
        for i in range(0,3): 
            if(i>=len(lst)):
                allFeatures.append('Empty')
            else:
                allFeatures.append(lst[i][0])
    else:
        # add the top 3 features. 
        allFeatures =[lst[0][0], lst[1][0],lst[2][0]]

    userShowReview = list(reversed(reviewList))
    if room != None:
        userImagesUnformated = room.images
        userImages = []
        for image in userImagesUnformated:
            userImages.append(image.filename)
    else:
        userImages = []
        # userImages.append("Images/main_DCC.jpg")
    if len(userImages) != 0:
        print("in other thing filename is", userImages[0])
    
    
    current_building = buildingName
    current_room = roomName

    if request.method == "POST": # this needs to render the createReview page - addReview.html using the correct building name and room name
        return redirect(url_for('views.createReview',buildingName=buildingName, roomName=roomName))

    
    
    # allReviews=[]
    # allPictures=[]

    #**locals() passes all the local variables defines in this function to room.html
    return render_template("room.html", **locals())


@views.route('/display_image/<filename>')
def display_image(filename):
    print("IN display_image filename is", filename)
    return redirect(url_for('static', filename=filename,code=301))



# this will return the correct number of stars for a review
def checkStars():
    stars = request.form.get("stars")
    if stars == None:
        return -1
    return 6 - int(stars)



# this is the python code for the HTML page to create a review
@views.route('/createReview/<buildingName>/<roomName>', methods=['GET', 'POST'])
def createReview(buildingName, roomName):
    current_building = buildingName
    current_room = roomName
    if request.method == "POST": # this is the post request for when the submit button was pressed
        # send review to database 
        review = request.form.get("reviewTextbox") 
        if review == "" or review == None:
            review = " "

        featureList = request.form.get("featureList")
        rating = round(checkStars(), 1)
        
        # create the review class for the database
        review_o = Review(id=time.time(),rating=rating, written_review=review, room_number=roomName, building_name=buildingName)
        db.session.add(review_o) # add to the database 
        db.session.commit()
        features = featureList.split(";") # split the user inputted features by ;
        featuresUpdated = []
        # get the room to add the review to to the database or add it if its not there
        room = db.session.query(Room.number, Room.building_name).filter_by(number=roomName, building_name=buildingName).first()
        if featureList!='':
            for f in features: # format the reviews so they look better on the page
                if f!='':
                    f = f.strip()
                    f = f.title()
                    featuresUpdated.append(f)
                    f_o = Feature(id=time.time(), description=f, room_number=roomName, building_name=buildingName)
                    db.session.add(f_o)
                    db.session.commit()
                

        # add image to the database
        uploadedFile = request.files["picTaken"]
        filename = uploadedFile.filename
        if filename != "" and not validate_image(filename):
            errorMessage("Wrong file format")
        if validate_image(filename): 
            image_id = str(time.time())
            file_name = image_id + '.png'
            exists = os.path.exists(imagePath)
            if not exists:
                os.makedirs(imagePath)
            uploadedFile.save(os.path.join(imagePath, file_name))
            image = Img(id=image_id, filename=file_name, room_number=roomName, building_name=buildingName)
            db.session.add(image)
            db.session.commit()

        # else flash a message 
        # move to the page that shows this room
        return redirect(url_for('views.viewRoom',buildingName=buildingName, roomName=roomName))

    return render_template("addReview.html", **locals())

    
