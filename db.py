from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder="static")
app.config["SECRET_KEY"] = "clothesuploadkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = "static/files"
db = SQLAlchemy(app)


def init_db():
    with app.app_context():
        db.create_all()
        db.session.commit()


if __name__ == "__main__":
    init_db()
