from flask import Blueprint

rooms = Blueprint('rooms', __name__)


@views.route('/', methods=['GET', 'POST'])
def homepage():
    return "<h1> Test </h1>"
    #return render_template("index.html")
