from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # take note here--init relationship here.  not a db field in User.  Define one-to-many in the one side
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().endcode('utf-8').hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s{}'.format(digest, size)

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

@login.user_loader
def load_user(id):
    return User.query.get(int(id))