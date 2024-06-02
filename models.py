from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.sql import func

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))
    date = db.Column(db.DateTime(timezone=True), default=func.now())

class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.LargeBinary, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)

class Outfit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    outfit_name = db.Column(db.String(100))
    top_color = db.Column(db.String(20))
    bottom_color = db.Column(db.String(20))
    outer_color = db.Column(db.String(20))
    shoe_color = db.Column(db.String(20))
    acc_color = db.Column(db.String(20))
