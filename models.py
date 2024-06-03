from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.sql import func

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(50))

class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.LargeBinary, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)

class Outfit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    outfit_name = db.Column(db.String(100))
    top_color = db.Column(db.String(20))
    bottom_color = db.Column(db.String(20))
    outer_color = db.Column(db.String(20))
    shoe_color = db.Column(db.String(20))
    acc_color = db.Column(db.String(20))
