"""Database models for users, posts, comments, and likes.

Defines the SQLAlchemy models for the blog application,
including user accounts, blog posts, comments on posts,
and likes on posts.
"""

from . import db
from sqlalchemy.sql import func
from flask_login import UserMixin


class User(db.Model, UserMixin):
    """database model for user."""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    image_file = db.Column(
        db.String(20), nullable=False, default='default.jpg'
    )
    date_created = db.Column(
        db.DateTime(timezone=True), default=func.now()
    )
    posts = db.relationship(
        'Post', backref='user', passive_deletes=True
    )
    comments = db.relationship(
        'Comment', backref='user', passive_deletes=True
    )
    likes = db.relationship(
        'Like', backref='user', passive_deletes=True
    )


class Post(db.Model):
    """database model for blog post."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), unique=False)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(
        db.DateTime(timezone=True), default=func.now()
    )
    author = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete="CASCADE"),
        nullable=False
    )
    comments = db.relationship(
        'Comment', backref='post', passive_deletes=True
    )
    likes = db.relationship(
        'Like', backref='post', passive_deletes=True
    )


class Comment(db.Model):
    """database model for blog comment."""

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), unique=False)
    date_created = db.Column(
        db.DateTime(timezone=True), default=func.now()
    )
    author = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete="CASCADE"),
        nullable=False
    )
    post_id = db.Column(
        db.Integer,
        db.ForeignKey('post.id', ondelete="CASCADE"),
        nullable=False
    )


class Like(db.Model):
    """database model for blog like."""

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(
        db.DateTime(timezone=True), default=func.now()
    )
    author = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete="CASCADE"),
        nullable=False
    )
    post_id = db.Column(
        db.Integer,
        db.ForeignKey('post.id', ondelete="CASCADE"),
        nullable=False
    )
