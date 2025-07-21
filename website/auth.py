
# import external libaries
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
# import database
from . import db
# import from .models user
from .models import User

# set auth blueprint
auth = Blueprint("auth", __name__)


# sign up route
@auth.route("/sign-up", methods=['GET', 'POST'])
# sign up function
# returns sign up page

def sign_up():
    # sign up function
    # returns sign up page
    return render_template("sign_up.html")

# login route
@auth.route("/login")
# login function
# returns login page
def login():
    return render_template("login.html")

# logout route
@auth.route("/logout")
# logout function
# returns logout page
def logout():
    return render_template("logout.html")