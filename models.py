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
    name = db.Column(db.String(100), nullable=False)
    top = db.Column(db.String(200), nullable=False)
    bottom = db.Column(db.String(200), nullable=False)
    outerwear = db.Column(db.String(200), nullable=False)
    shoes = db.Column(db.String(200), nullable=False)
    bags = db.Column(db.String(200), nullable=False)
    accessories = db.Column(db.String(200), nullable=False)
