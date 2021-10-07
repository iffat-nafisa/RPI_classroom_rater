


class Photo:
	# not sure what needs to be here yet. This will store the information on a photo and the photo itself.
	# maybe store this in code with just a link to a file?
	pass




class Building:
	buildingName = ""
	roomList = [] 
	buildingLocationData = [] 

	def numRooms():
		return len(roomList)



class Room:
	roomNumber = 0
	building = Building()
	mainRoomPhoto = Photo() # this is the photo that can go with the room when it is searched 
	roomPhotos = []
	roomReviews = []

	def numReviews():
		return len(roomReviews)

	def numPhotos():
		return len(roomPhotos)



class Review:
	reviewerUserName = "Anonymous" # this is the default for when a user is not logged in
	room = Room() # the room that the review is for 
	reviewText = "" # the actual review
	reviewPhotos = [] # any photos that go with the review
	specialFeatures = [] # a list of special features that the room has
	numStars = 0; # the number of stars a room has out of 5.

