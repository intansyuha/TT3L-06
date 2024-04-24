from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(8), nullable=False)
    password = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(50), nullable=False)