from flask_login import UserMixin
from initialize import db

# user db class
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100))
    name = db.Column(db.String(100))
    course = db.Column(db.String(100))
    prof = db.Column(db.String(100))
    date = db.Column(db.DateTime)
    file = db.Column(db.String(100), unique=True)

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100))
    assignment = db.Column(db.Integer)
    upvote = db.Column(db.Integer)
    downvote = db.Column(db.Integer)
    response = db.Column(db.String(2000))