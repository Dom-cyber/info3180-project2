import os
import jwt
import random
import time
from app import app
from app import db
from app import csrf
from datetime import datetime
from app.forms import RegistrationForm, PostForm, LoginForm
from flask import render_template, flash, request,make_response, redirect, url_for, jsonify, json,session
from app.models import Users, Posts, Likes, Follows
from flask_login import current_user, login_user,logout_user
from sqlalchemy import desc
from werkzeug.utils import secure_filename
from functools import wraps
from flask import _request_ctx_stack


def requires_auth(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    auth = request.headers.get('Authorization', None)
    if not auth:
      return jsonify({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'}), 401

    parts = auth.split()

    if parts[0].lower() != 'bearer':
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'}), 401
    elif len(parts) == 1:
      return jsonify({'code': 'invalid_header', 'description': 'Token not found'}), 401
    elif len(parts) > 2:
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'}), 401

    token = parts[1]
    try:
         payload = jwt.decode(token, app.config['SECRET_KEY'])

    except jwt.ExpiredSignature:
        return jsonify({'code': 'token_expired', 'description': 'token is expired'}), 401
    except jwt.DecodeError:
        return jsonify({'code': 'token_invalid_signature', 'description': 'Token signature is invalid'}), 401

    return f(*args, **kwargs)
  return decorated_function

@app.route('/api/users/register', methods=['POST'])
def register():
    form = RegistrationForm()
    if request.method=="POST" and form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        firstname=form.firstname.data
        lastname=form.lastname.data
        location=form.location.data
        email=form.email.data
        biography=form.biography.data
        photourl=form.photo.data 
        filename=secure_filename(photourl.filename)
        photourl.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        user = Users(firstname,lastname,username,email,location,biography,filename)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User successfully registered"}) 
    return jsonify(error= form_errors(form)),201



@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    """
    Because we use HTML5 history mode in vue-router we need to configure our
    web server to redirect all routes to index.html. Hence the additional route
    "/<path:path".
    Also we will render the initial webpage and then let VueJS take control.
    """
    return render_template('index.html')


def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages


#The functions below should be applicable to all Flask apps.
@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")