from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    jsonify,
    flash,
    url_for,
    send_from_directory,
)
from flask_wtf import FlaskForm
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import FileField, SubmitField, SelectField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired
from db import db, init_db  # Import init_db to initialize the database
from rembg import remove
from models import User, Img, Outfit
import os
from PIL import Image

app = Flask(__name__, static_folder="static")
app.config["SECRET_KEY"] = "clothesuploadkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = "static/files"
db.init_app(app)


class UploadClothesForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    category = SelectField(
        "Category",
        choices=[
            ("top", "Top"),
            ("bottom", "Bottom"),
            ("outerwear", "Outerwear"),
            ("shoes", "Shoes"),
            ("accessories", "Accessories"),
        ],
        validators=[InputRequired()],
    )
    submit = SubmitField("Upload File")


@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
@app.route("/login.html", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session["email"] = email
            session["username"] = user.username
            return redirect(url_for("community_page", username=user.username))

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
@app.route("/signup.html", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()

        if existing_user:
            flash("Username or email already exists.", "error")
            return render_template(
                "signup.html"
            )  # Re-render the signup form with error message
        else:
            current_user = User(username=username, email=email, password=password)
            db.session.add(current_user)
            db.session.commit()
            flash("Registration successful!", "success")
            return redirect("/login")  # Redirect to login after successful registration

    return render_template("signup.html")


@app.route("/save_outfit", methods=["POST"])
def save_outfit():
    try:
        data = request.get_json()
        data["email"] = session.get("email")
        outfit = Outfit(**data)
        db.session.add(outfit)
        db.session.commit()
        return jsonify({"message": "Outfit saved successfully"})
    except Exception as e:
        app.logger.error(f"Error saving outfit: {str(e)}")
        return jsonify({"error": "Failed to save outfit"}), 400


@app.route("/get_outfit", methods=["GET"])
def get_outfit():
    outfits = Outfit.query.all()
    outfits_list = [
        {
            "id": outfit.id,
            "name": outfit.name,
            "top": outfit.top,
            "bottom": outfit.bottom,
            "outerwear": outfit.outerwear,
            "shoes": outfit.shoes,
            "bags": outfit.bags,
            "accessories": outfit.accessories,
        }
        for outfit in outfits
    ]
    return jsonify(outfits_list)


@app.route("/delete_outfit/<int:outfit_id>", methods=["DELETE"])
def delete_outfit(outfit_id):
    try:
        outfit = Outfit.query.get(outfit_id)
        if outfit:
            db.session.delete(outfit)
            db.session.commit()
            return jsonify({"message": "Outfit deleted successfully"}), 200
        else:
            return jsonify({"message": "Outfit not found"}), 404
    except Exception as e:
        app.logger.error(f"Error deleting outfit: {str(e)}")
        return jsonify({"error": "Failed to delete outfit"}), 400


@app.route("/outfitgallery")
@app.route("/outfitgallery.html")
def outfit_gallery():
    if "email" not in session:
        outfits = Outfit.query.all()
        return redirect(url_for("login"))
    return render_template("outfitgallery.html", username=session["username"])


@app.route("/community-page")
@app.route("/community-page.html")
def community_page():
    if "email" not in session or "username" not in session:
        return redirect(url_for("login"))
    username = session.get("username")
    return render_template("community-page.html", username=username)


@app.route("/outfitcreator", methods=["GET", "POST"])
@app.route("/outfitcreator.html")
def outfit_creator():
    if not session.get("email"):
        return redirect("/login")

    image_urls = session.get("image_urls", {})
    return render_template(
        "outfitcreator.html", image_urls=image_urls, username=session["username"]
    )


@app.route("/settings")
@app.route("/settings.html")
def settings():
    if "email" not in session:
        return redirect(url_for("login"))
    return render_template("settings.html", username=session["username"])


@app.route("/index", methods=["GET", "POST"])
@app.route("/index.html", methods=["GET", "POST"])
def index():
    form = UploadClothesForm()
    file_url = None
    if request.method == "POST" and form.validate_on_submit():
        if session.get("email"):
            file = form.file.data  # grab file
            filename = secure_filename(file.filename)
            file_url = url_for("get_file", filename=filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)  # save file
            file.save(file_path)

            with open(file_path, "rb") as input_file:
                input_data = input_file.read()

            output_data = remove(input_data)

            process_filename = filename
            process_file_path = os.path.join(
                app.config["UPLOAD_FOLDER"], process_filename
            )

            with open(process_file_path, "wb") as output_file:
                output_file.write(output_data)

            mimetype = file.mimetype
            category = form.category.data  # Obtain category from the form
            email = session.get("email")  # Get email from session

            img = Img(
                data=output_data,
                mimetype=mimetype,
                name=filename,
                category=category,
                email=email,
            )
            db.session.add(img)
            db.session.commit()

            return redirect(url_for("imgwindow", filename=process_filename))
    return render_template("index.html", form=form, file_url=file_url)


@app.route("/uploads/<filename>")
def get_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/imgwindow/<filename>", methods=["GET", "POST"])
def imgwindow(filename):
    file_url = url_for("get_file", filename=filename)
    return render_template("imgwindow.html", file_url=file_url)


@app.route("/wardrobecategory", methods=["GET", "POST"])
@app.route("/wardrobecategory.html")
def wardrobecategory():
    if "email" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        category = request.form.get("category").lower()
        file_url = request.form.get("file_url")

        if "image_urls" not in session:
            session["image_urls"] = {}

        if category not in session["image_urls"]:
            session["image_urls"][category] = []

        session["image_urls"][category].append(file_url)
        session.modified = True

        app.logger.debug(f"Session image URLs: {session['image_urls']}")

    image_urls = session.get("image_urls", {})
    return render_template(
        "wardrobecategory.html",
        category=request.form.get("category", "").lower(),
        file_url=request.form.get("file_url", ""),
        image_urls=image_urls,
    )


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
