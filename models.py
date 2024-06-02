from . import db
import bcrypt
from sqlalchemy.sql import func

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(8), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(50))

    def __init__(self, email, password, username):
        self.username = username
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

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
