from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("outfitcreator.html")


@app.route("/outfitgallery.html")
def outfit_gallery():
    return render_template("outfitgallery.html")


if __name__ == "__main__":
    app.run(debug=True)
