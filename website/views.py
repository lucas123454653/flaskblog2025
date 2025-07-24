import os 
from pathlib import Path
from PIL import Image
import secrets
from flask_login import login_user, logout_user, login_required, current_user

# import external libraries
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify


#import database
from . import db

# import from .models user
from .models import User, Post, Comment, Like
# Form for updating user profile
from .forms import UpdateAccountForm, RegistrationForm
# import from .forms
from .forms import PostForm

# set views blueprint
views = Blueprint("views", __name__)


# default/home route
@views.route("/")
@views.route("/home")
# home route function
# returns home.html
def home():
    return render_template("home.html", user=current_user)


# blog page route
@views.route("/blog")
#user must be logged in to post
@login_required
# home route function
# returns home.html
def blog():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_created.desc()).paginate(page=page, per_page=4)
    return render_template("blog.html", user=current_user, posts=posts)


# create blog post route
@views.route("/create-post", methods=['GET','POST'])
#user must be logged in to post
@login_required
def create_post():
    if request.method == "POST":
        title = request.form.get('title')
        content = request.form.get('content')
        if not title:
            flash("Title cannot be empty.", category="error")
        elif not content:
            flash("Blog cannot be empty.", category="error")
        else:
            post = Post(title=title, content=content, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.blog'))

    return render_template("create_post.html", user=current_user)


# delete blog post route
@views.route("/delete-post/<id>")
#user must be logged in to post
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    if not post: 
        flash('Post does not exist', category="error")
    elif current_user.id != post.author:
        flash('You do not have permission to delete this post', category="error") 
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted!', category='success')
    return redirect(url_for('views.blog'))

# update blog post route
@views.route("/update-post/<id>", methods=['GET', 'POST'])
#user must be logged in to post
@login_required
def update_post(id):
    post = Post.query.filter_by(id=id).first()
    if post.author != current_user.id:
        flash("You cannot edit this post!", category="error")
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Post updated", category="success")
        page = request.args.get('page', 1, type=int)
        posts = Post.query.order_by(Post.date_created.desc()).paginate(page=page, per_page=4)
        return render_template("blog.html", user=current_user, posts=posts)

    elif request.method =='GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template("update_post.html", form=form, user=current_user, posts=post)





# view user posts route
@views.route("/posts/<username>")
@login_required
def posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('No user with that username exists', category="error") 
        return redirect(url_for('views.blog'))
    #posts = user.posts
    posts = Post.query.filter_by(user=user).order_by(Post.date_created.desc()).paginate(page=page, per_page=4)
    return render_template("posts.html", user=current_user, posts=posts, username=username)



# blog comment route
@views.route("/create-comment/<post_id>", methods=['POST'])
#user must be logged in to post
@login_required
def create_comment(post_id):
    text = request.form.get('text')
    if not text:
        flash('Comment cannot be empty', category="error")
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
            flash("Comment added!", category="success")
        else:
            flash("Post does not exist", category="error")

    return redirect(url_for("views.blog"))



# delete comment post route
@views.route("/delete-comment/<comment_id>")
#user must be logged in to post
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    if not comment: 
        flash('comment does not exist', category="error")
    elif current_user.id != comment.author and current_user.id != comment.post.author:      
        flash('You do not have permission to delete this comment', category="error") 
    else:
        db.session.delete(comment)
        db.session.commit()
        flash('Comment deleted!', category='success')
    return redirect(url_for('views.blog'))



# like comment route
@views.route("/like-post/<post_id>", methods=['POST'])
#user must be logged in to post
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(author=current_user.id, post_id=post_id).first()
    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else: 
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    return jsonify({"likes": len(post.likes), "liked": current_user.id in map(lambda x: x.author, post.likes)})

#making profile pics random id
def save_picture(form_picture):
    path = Path("website/static/profile_pics")
    random_hex = secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(path, picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@views.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', user=current_user, image_file=image_file, form=form)