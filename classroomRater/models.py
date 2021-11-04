from sqlalchemy import Column, ForeignKey, Integer, Unicode
from sqlalchemy.orm import backref, relationship
from app import db
from sqlalchemy.sql import func


class School(db.Model):
    name = db.Column(db.String(300), primary_key=True)
    buildings = db.relationship('Building')

class Building(db.Model):
    name = db.Column(db.String(150), primary_key=True)
    school_name = db.Column(db.String(300), db.ForeignKey('school.name'))
    rooms = db.relationship('Room', backref='building')

class Room(db.Model):
    number = db.Column(db.Integer, primary_key=True)
    building_name = db.Column(db.String(300), db.ForeignKey('building.name'))
    reviews = db.relationship('Review', backref='room')
    images = db.relationship('Img', backref='room')

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    written_review = db.Column(db.String(100000))
    written_review = db.Column(db.DateTime(timezone=True), default=func.now()) 
    room_number = db.Column(db.Integer, db.ForeignKey('room.number'))

class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    room_number = db.Column(db.Integer, db.ForeignKey('room.number'))
    
class Feature(db.Model):
    description = db.Column(db.String(150), primary_key=True)
    # need to figure out many to many relationship 