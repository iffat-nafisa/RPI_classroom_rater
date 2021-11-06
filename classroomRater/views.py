from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Room


#Create Blueprint
views = Blueprint('views', __name__)

#This function will run whenever go to the "/" root
@views.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == "POST":
        building = request.form.get("building")
        room_no = request.form.get("room")
        room_exists = db.session.query(Room.number).filter_by(number=room_no).count()
        if room_exists > 0:
            return redirect(url_for('rooms.viewRoom'))
        room = Room(number=room_no, building_name=building)
        db.session.add(room)
        db.session.commit()
        return redirect(url_for('rooms.viewRoom'))

    return render_template("index.html")