from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, BooleanField, TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from flask_wtf.file import FileField, FileRequired, FileAllowed
from app.models import Users
from flask import request

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	firstname = StringField('FirstName')
	lastname = StringField('LastName')
	email = StringField('Email', validators=[DataRequired(), Email()])
	location = StringField('Location', validators=[DataRequired()])
	biography = TextAreaField('Biography', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	photo = FileField('Profile Picture', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'Images only!'])])


