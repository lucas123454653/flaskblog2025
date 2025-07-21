
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
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

    email_exists = User.query.filter_by(email=email).first()
    username_exists = User.query.filter_by(username=username).first()

    if email_exists:
        flash('Email is already in use.', category='error')
    elif username_exists:
        flash('Username is already in use.', category='error')
    elif password1 != password2:
        flash('Passwords do not match!', category='error')
    elif len(password1) < 8:
        flash('Passwords is too short', category='error')
    elif len(username) < 2:
        flash('Username is too short', category='error')
    elif len(email) < 4:
        flash('Email is not valid', category='error')
    else:
        new_user = User(email=email, username=username, password=generate_password_hash(password1, method='scrypt:32768:8:1'))
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        flash('Your account has been created!', category='success')
        return redirect(url_for('views.home'))

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