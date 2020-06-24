from flask_wtf import FlaskForm
from app.models import Users
from flask import request
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, PasswordField, FileField
from wtforms.validators import DataRequired, Email, ValidationError



class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    firstname= StringField('Firstname')
    lastname= StringField('Lastname')
    email = StringField('Email', validators=[DataRequired(), Email()])
    location = StringField('Location', validators=[DataRequired()])
    biography = TextAreaField('Biography', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    photo = FileField('Display Picture', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'Images only!'])])


    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Invalid! Please choose a different username.')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Invalid! Please choose a different email address.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class PostForm(FlaskForm):
    photo = FileField('Photo', validators=[FileRequired(), FileAllowed(['jpg','jpeg','png', 'Images only!']) ])
    caption = StringField('Caption', validators=[DataRequired()])