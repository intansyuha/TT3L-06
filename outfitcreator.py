from flask import Flask, render_template
from db import app as db_app

app = Flask(__name__)
app.register_blueprint(db_app)


@app.route("/")
def home():
    return render_template("outfitcreator.html")


@app.route("/outfitgallery.html")
def outfit_gallery():
    return render_template("outfitgallery.html")


if __name__ == "__main__":
    app.run(debug=True)
