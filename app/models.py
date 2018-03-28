from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

# followers table - an example of many to many
# as this is an auxiliary table with no data other than foreign keys
# it is not created with a model class

followers = db.Table('followers',
                      db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                      db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
                     )

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # take note here--init relationship here.  not a db field in User.  Define one-to-many in the one side
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    # define follower-followed many to many relationship.  Note it is self referential, so
    # both 'left side' entity (from class User-follower) and 'right side' entity, from arg passed to db.relationship-followed
    # are User
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id ==id),
        secondaryjoin=(followers.c.followed_id ==id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    # filter allows arbitrary condition unlike filter_by
    # here checking for items that have left side foreign key set to self
    # and right side set to user argument passed to the func
    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    # query that joins Post table with followers where the person being followed equals the author
    # then filtered down to those entries where the follower is the user (self) and sorted
    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())


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