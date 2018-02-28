from datetime import datetime
from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic') # take note here--init relationship here.  not a db field in User.  Define one-to-many in the one side

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

# test class to begin to figure out how to translate this to shift info
# need to figure out ORM/database structure to make sure this is query-able
# for usefulness and for later data viz/analysis
# ?? should i create a primary key integer and have date as a separate col?
# class Shift(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    date = db.Column(db.DateTime, default=datetime.utcnow)
#    tips = db.Column(db.Float)