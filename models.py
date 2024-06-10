from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import bcrypt
from datetime import datetime
from db import db


class User(db.Model, UserMixin):
    __tablename__ = 'User'  
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(50))

    def __init__(self, email, password, username):
        self.username = username
        self.email = email
        self.password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

    def check_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))


class Img(db.Model):
    __tablename__ = "Img"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)


class Outfit(db.Model):
    __tablename__ = "Outfit"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    top = db.Column(db.String(200), nullable=False)
    bottom = db.Column(db.String(200), nullable=False)
    outerwear = db.Column(db.String(200), nullable=False)
    shoes = db.Column(db.String(200), nullable=False)
    bags = db.Column(db.String(200), nullable=False)
    accessories = db.Column(db.String(200), nullable=False)

class Feed(db.Model):
    __tablename__ = 'Feed'  
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    outfit_id = db.Column(db.Integer, db.ForeignKey('outfit.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now())