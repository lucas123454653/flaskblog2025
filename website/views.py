from flask_login import login_user, logout_user, login_required, current_user

# import external libraries
from flask import Blueprint, render_template, request, flash, redirect, url_for
#import database
from . import db
# import from .models user
from .models import User, Post
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
    if request.method == "POST":
        title = request.form.get('title')
        content = request.form.get('content')
        
        if not title:
            flash('Title cannot be empty.')
        elif not content:
            flash('Blog cannot be empty.')
        else:
            post = User(title=title, content=content, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.home'))

        


    return render_template("create_post.html", user=current_user)