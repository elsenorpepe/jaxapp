from app import db
from sqlalchemy import func

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

# test class to begin to figure out how to translate this to shift info
# need to figure out ORM/database structure to make sure this is query-able
# for usefulness and for later data viz/analysis
class Shift(db.Model):
    __tablename__ = 'shift'
    date = db.Column(db.DateTime, default =func.now(), primary_key=True)
    tips = db.Column(db.Float) # ?? should i create a primary key integer and have date as a separate col?