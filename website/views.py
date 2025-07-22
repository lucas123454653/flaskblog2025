from flask_login import login_user, logout_user, login_required, current_user


# import external libraries
from flask import Blueprint, render_template


# set views blueprint
views = Blueprint("views", __name__)

# default/home route
@views.route("/")
@views.route("/home")
# home route function
# returns home.html
def home():
    return render_template("home.html", user=current_user)