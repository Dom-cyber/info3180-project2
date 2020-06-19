from flask_wtf import FlaskForm
from flask import request
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FileField,SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileField, FileRequired, FileAllowed
from app.models import Users


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    firstname= StringField('Firstname')
    lastname= StringField('Lastname')
    email = StringField('Email', validators=[DataRequired(), Email()])
    location = StringField('Location', validators=[DataRequired()])
    biography = TextAreaField('Biography', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    photo = FileField('Profile Photo', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'Images only!'])])


    


    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username invalid!.')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Username invalid!.')


