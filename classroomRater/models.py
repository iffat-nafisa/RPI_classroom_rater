from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, Unicode
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql import func

db = SQLAlchemy()
DB_NAME = 'classroomrater.db'

# DB model for school
# A school has a name and buildings within it
# (NAME, buildings)
class School(db.Model):
    name = db.Column(db.String(300), primary_key=True)
    buildings = db.relationship('Building')

# DB model for building
# A building has a name, belongs to a school, and has rooms within it
# (NAME, SCHOOL_NAME, rooms)
class Building(db.Model):
    name = db.Column(db.String(150), primary_key=True)
    school_name = db.Column(db.String(300), db.ForeignKey('school.name'))
    rooms = db.relationship('Room', backref='building')

# DB model for a room
# A room has a room number, the name of the building it's in, and reviews and images associated with it
# (NUMBER, BUILDING_NAME, reviews, images) 
class Room(db.Model):
    number = db.Column(db.Integer, primary_key=True)
    building_name = db.Column(db.String(300), db.ForeignKey('building.name'))
    reviews = db.relationship('Review', backref='room')
    images = db.relationship('Img', backref='room')
    images = db.relationship('Feature')


# DB model for a review
# A review has an id, rating, text, and the room it's associated with
# (ID, rating, written_review, ROOM_NUMBER)
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    written_review = db.Column(db.String(100000))
    room_number = db.Column(db.Integer, db.ForeignKey('room.number'))

# DB model for an image
# An image has an id, its contents, a name, a mimetype, and the room it's associated with
# (ID, img, name, mimetype, ROOM_NUMBER)
class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    room_number = db.Column(db.Integer, db.ForeignKey('room.number'))
    
# NEED TO COMMENT AFTER FIGURING OUT
class Feature(db.Model):
    description = db.Column(db.String(150), primary_key=True)
    room_number = db.Column(db.Integer, db.ForeignKey('room.number'))

    # need to figure out many to many relationship 

# Add schools and buildings to database
def addSchoolAndBuildings():
    # declare a list of all buildings within RPI
    buildingList = ["DCC", "SAGE", "Amos Eaton Hall", "Carnegie Building", "Center for Biotechnology and Interdisciplinary Studies", "CBIS", "Chapel + Cultural Center", "Experimental Media and Performing Arts Center", "EMPAC", "Folsom Library", "Greene Building","Gurley Building", "Hirsch Observatory", "Houston Field House", "Jonsson Engineering Center", "Low Center", "West Hall", "Winslow Building"]
    schoolName = "Rensselaer Polytechnic Institute"

    # add school to the database if they don't exist
    school_exists = db.session.query(School.name).filter_by(name=schoolName).count()
    if school_exists == 0:
        school = School(name=schoolName)
        db.session.add(school) # add to the database 
        db.session.commit() 

    # add buildings to the database if they don't exist
    for b in buildingList:
        building_exists = db.session.query(Building.name).filter_by(name=b).count()
        if building_exists == 0:
            building = Building(name=b, school_name=schoolName)
            db.session.add(building) # add to the database 
            db.session.commit() 
