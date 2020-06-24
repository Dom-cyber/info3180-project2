from datetime import datetime
from app import db,login
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5



class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total



class Users(db.Model, UserMixin,SearchableMixin):
    __searchable__ = ['username']
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(180))
    lastname = db.Column(db.String(180))
    username = db.Column(db.String(55), index=True, unique=True)
    email = db.Column(db.String(130), index=True, unique=True)
    password = db.Column(db.String(180))
    biography = db.Column(db.String(350))
    location = db.Column(db.String(200))
    display_photo  = db.Column(db.String(350))
    joined_on = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    

    
    def __init__(self,firstname, lastname, username, email,location,biography, imgProfile):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email
        self.biography = biography
        self.display_photo = imgProfile
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



@login.user_loader
def load_user(id):
    return Users.query.get(int(id))

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.String(300))
    created_on = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    caption=db.Column(db.String(300))
    user_id = db.Column(db.Integer)
    

    def __init__(self,user_id, photo, caption):
        self.user_id = user_id
        self.photo = photo
        self.caption = caption
    


    def __repr__(self):
        return '<Post {}>'.format(self.img)

    
class Likes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    post_id = db.Column(db.Integer)
    def __init__(self,userid,post_id):
        self.user_id=userid
        self.post_id=post_id

    def __repr__(self):
        return '<Likes {}>'.format(self.id)

class Follows(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    follower_id  = db.Column(db.Integer)

    def __init__(self,userid,follower_id):
        self.user_id=userid
        self.follower_id=follower_id

    def __repr__(self):
        return '<Likes {}>'.format(self.id)