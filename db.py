from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///outfits.db"
db = SQLAlchemy(app)


# Define your Outfit model here
class Outfit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    outfit_name = db.Column(db.String(100))
    top_color = db.Column(db.String(20))
    bottom_color = db.Column(db.String(20))
    outer_color = db.Column(db.String(20))
    shoe_color = db.Column(db.String(20))
    acc_color = db.Column(db.String(20))


def init_db():
    with app.app_context():
        db.create_all()


if __name__ == "__main__":
    init_db()

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def db_init(app):
    db.init_app(app)

    with app.app_context():
        db.create_all()
