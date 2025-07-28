"""Forms for user registration, posting, and account updating.

Includes form validation to ensure unique usernames and emails.
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import (
    StringField, SubmitField, TextAreaField, PasswordField
)
from wtforms.validators import (
    DataRequired, Length, ValidationError, EqualTo, Email
)
from .models import User


class RegistrationForm(FlaskForm):
    """Form for users to create a new account."""

    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Sign Up')


class PostForm(FlaskForm):
    """Form to create a new post."""

    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


class UpdateAccountForm(FlaskForm):
    """Form to update user's account details."""

    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField(
        'Update Profile Picture',
        validators=[FileAllowed(['jpg', 'png'])]
    )
    submit = SubmitField('Update')

    def validate_username(self, username):
        """Validate that the username is not already taken by another user."""
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'That username is already taken. '
                    'Please choose a different one.'
                )

    def validate_email(self, email):
        """Validate that the email is not already taken by another user."""
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'That email is already taken. '
                    'Please choose a different one.'
                )
