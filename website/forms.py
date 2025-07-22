from flask_wtf import FlaskForm
from flask_wtf.file import current_user
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, length, ValidationError
from .models import User




class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('post')