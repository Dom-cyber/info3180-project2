from datetime import datetime
from app import db,login
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5



class Users(db.Model, UserMixin,SearchableMixin):
    __searchable__ = ['username']
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(150))
    lastname = db.Column(db.String(140))
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(300))
    biography = db.Column(db.String(140))
    location = db.Column(db.String(150))
    profile_photo  = db.Column(db.String(300))
    joined_on = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    
    
    def __init__(self,firstname, lastname, username, email,location,biography, imgProfile):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email
        self.biography = biography
        self.profile_photo = imgProfile
        self.location=location
    


    def __repr__(self):
        return '<Users {}>'.format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

   
    def like_post(self, post):
        if not self.post_liked(post):
            like = Likes(user_id=self.id, post_id=post.id)
            db.session.add(like)

    def dislike_post(self, post):
        if self.post_liked(post):
            Likes.query.filter_by(user_id=self.id, post_id=post.id).delete()

    def post_liked(self, post):
        return Likes.query.filter(Likes.user_id == self.id,
               Likes.post_id == post.id).count() > 0
    

    def __init__(self,user_id, photo, caption):
        self.user_id = user_id
        self.photo = photo
        self.caption = caption
    


    def __repr__(self):
        return '<Post {}>'.format(self.img)

    


    def __repr__(self):
        return '<Likes {}>'.format(self.id)