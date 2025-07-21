
# import external libaries
from flask import Blueprint, render_template

# set auth blueprint
auth = Blueprint("auth", __name__)


# sign up route
@auth.route("/sign-up", methods=['GET', 'POST'])
# sign up function
# returns sign up page
def sign_up():
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