from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__, static_folder="static")
app.config["SECRET_KEY"] = "clothesuploadkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = "static/files"
db = SQLAlchemy(app)


class User(db.Model):
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


class Outfit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    top = db.Column(db.String(200), nullable=False)
    bottom = db.Column(db.String(200), nullable=False)
    outerwear = db.Column(db.String(200), nullable=False)
    shoes = db.Column(db.String(200), nullable=False)
    bags = db.Column(db.String(200), nullable=False)
    accessories = db.Column(db.String(200), nullable=False)


class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.LargeBinary, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)


def init_db():
    with app.app_context():
        db.create_all()
        db.session.commit()


if __name__ == "__main__":
    init_db()
