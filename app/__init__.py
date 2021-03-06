import os
import psycopg2
from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect 
from flask_sqlalchemy import SQLAlchemy
from flask import render_template



app = Flask(__name__)
SQLALCHEMY_DATABASE_URI ="postgresql://project2:Temp1234@localhost/project2"
SQLALCHEMY_TRACK_MODIFICATIONS = False

UPLOAD_FOLDER = "./app/static/uploads"
SECRET_KEY = 'Sup3r$3cretkey'

app.config.from_object(__name__)
csrf = CSRFProtect(app)
db = SQLAlchemy(app)

login = LoginManager(app) 
login.init_app(app)
login.login_view = 'login'

from app import views


