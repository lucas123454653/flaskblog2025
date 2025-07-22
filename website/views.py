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


# create blog post route
@views.route("/create-post", methods=['GET','POST'])
@login_required
# create blog post route function
# returns create_post.html
def create_post():
    return render_template("create_post.html", user=current_user)