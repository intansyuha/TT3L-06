# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import bcrypt
from werkzeug.security import generate_password_hash


db = SQLAlchemy()

class User(db.Model, UserMixin):
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
        try:
            return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))
        except ValueError:
            print(f"Invalid salt for user {self.email}")
            return False


class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)

class Outfit(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    top = db.Column(db.String(200), nullable=False)
    bottom = db.Column(db.String(200), nullable=False)
    outerwear = db.Column(db.String(200), nullable=False)
    shoes = db.Column(db.String(200), nullable=False)
    bags = db.Column(db.String(200), nullable=False)
    accessories = db.Column(db.String(200), nullable=False)
    published = db.Column(db.Boolean, default=False)

class Feed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15))
    outfit_id = db.Column(db.Integer, db.ForeignKey('outfit.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now())
    outfit = db.relationship('Outfit', backref='feeds')
    caption = db.Column(db.String(100))