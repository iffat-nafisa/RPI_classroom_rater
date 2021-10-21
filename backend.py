import squilt3
import re


dbpath="room_list.db"


def regex(buildings, search):
	pass

	

def insert_date(dbpath,add_room):
	conn=squilt3.connect(dbpath) #set up connection
	cursor=conn.cusor()   #open the 
	sql='insert into room_list (building_name, room_number)'\
		'values(?,?,?)'
	cur.execute(sql,data)
	conn.commit()
	cur.close()
	conn.close()  #this function is for add new room

def insert_mult_date(dbpath,room_list):
	conn=squilt3.connect(dbpath) #set up connection
	cursor=conn.cusor()   #open the 
	sql='insert into room_list (building_name, room_number)'\
		'values(?,?,?)'
	cur.executemany(sql,data_list)
	conn.commit()
	cur.close()
	conn.close() #this function is for set up the database

class school:
	schoolName = ""
	buildingList = [] # a list of all the buildings in the school


	# this will return a building based on the passed in name
	def getBuildingByName(buildingName):
		for building in buildingList:
			if (building.buildingName == buildingName):
				return building

	# this will return a list of buildings that contain the passed in room
	def getBuildingByRoom(roomName):
		foundBuildings = []
		for building in buildingList:
			if (building.roomList.contains(roomName)):
				buildingList.append(building)
		return foundBuildings



class Photo:
	name = ""
	filePath = "" # this will be the path to the file to use in HTML


class Building:
	buildingName = ""
	roomList = [] # a list of all the rooms in that building
	buildingStreetAddress = ""


	# this will return the total number of rooms
	def numRooms():
		return len(roomList)


	# this function will find a single room using the room number
	def getRoomByNumber(roomNumber): 
		for room in roomList:
			if (room.roomNumber == roomNumber):
				return room


	# this will return all the rooms with the passed in feature
	def getRoomsByFeature(feature): 
		foundRooms = []
		for room in roomList:
			if room.hasFeature(feature):
				foundRooms.append(room)
		return foundRooms


	# this will return all the rooms >= the number of passed in stars
	def getRoomsByStars(numStars): 
		foundRooms = []
		for room in roomList:
			if room.numStars >= numStars:
				foundRooms.append(room)
		return foundRooms




class Room:
	roomNumber = 0
	building = Building()
	mainRoomPhoto = Photo() # this is the photo that can go with the room when it is searched 
	roomPhotos = [] 
	specialFeatures = [] # this is a list of the rooms special features

	# the _ means do not directly mess with these outside of this class. Private vars
	_roomReviews = [] # this is because we dont want to add a review without running the function
	_totalStars = 0 # this is because it is useless without averageStars function


	def numReviews():
		return len(_roomReviews)

	def numPhotos():
		return len(roomPhotos)

	def findReviewsByStars(numStars): # this function will return the reviews that are equal to or above the number of passed in stars
		foundReviews = []
		for review in _roomReviews:
			if (review.numStars >= numStars):
				foundReviews.append(review)
		return foundReviews

	def findReviewsByUser(username): # this function will return the reviews from the passed in user
		foundReviews = []
		for review in _roomReviews:
			if (review.username == username):
				foundReviews.append(review)
		return foundReviews


	# this will return the average number of stars for this room
	def averageStars():
		return _totalStars/numReviews()


	# this function will correctly add a review to the list of reviews, and update all other things in the room
	def addReview(review):
		totalStars+=review.numStars # add the stars
		for feature in review.specialFeatures: # add new special features
			if not specialFeatures.contains(feature):
				specialFeatures.append(feature)

		_roomReviews.append(review) # add the review


	def hasFeature(feature):
		if (specialFeatures.contains(feature)):
			return True
		return False


	def getReviews():
		return _roomReviews





class Review:
	reviewerUsername = "Anonymous" # this is the default for when a user is not logged in
	room = Room() # the room that the review is for 
	reviewText = "" # the actual review
	reviewPhotos = [] # any photos that go with the review
	specialFeatures = [] # a list of special features that the room has
	numStars = 0; # the number of stars a room has out of 5.


