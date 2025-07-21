from . import db
from sqlalchemy.sql import func
from flask_login import UserMixin




class User(db.model, UserMixin):
    id = db.Column(db.Interger, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unqiue=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())