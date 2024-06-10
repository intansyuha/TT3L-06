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

        # Ensure data integrity before saving
        required_fields = [
            "name",
            "top",
            "bottom",
            "outerwear",
            "shoes",
            "bags",
            "accessories",
        ]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        outfit = Outfit(**data)
        db.session.add(outfit)
        db.session.commit()

        app.logger.debug(f"Outfit saved: {outfit}")

        return jsonify({"message": "Outfit saved successfully"})
    except Exception as e:
        app.logger.error(f"Error saving outfit: {str(e)}")
        return jsonify({"error": "Failed to save outfit"}), 400


@app.route("/get_outfit", methods=["GET"])
def get_outfit():
    email = session.get("email")
    if not email:
        return jsonify({"error": "Unauthorized"}), 401

    outfits = Outfit.query.filter_by(email=email).all()

    if not outfits:
        return jsonify({"message": "No outfits found for the specified email"}), 404

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


@app.route("/delete_image/<filename>", methods=["DELETE"])
def delete_image(filename):
    email = session.get("email")
    if not email:
        app.logger.error("Unauthorized access attempt.")
        return jsonify({"error": "Unauthorized"}), 401

    app.logger.info(f"Attempting to delete image: {filename} for user: {email}")
    img = Img.query.filter_by(email=email, name=filename).first()
    if img:
        app.logger.info(f"Image found in database: {img.name}")
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], img.name)
        if os.path.exists(file_path):
            app.logger.info(f"Image found in filesystem: {file_path}")
            os.remove(file_path)
        else:
            app.logger.warning(f"Image not found in filesystem: {file_path}")

        db.session.delete(img)
        db.session.commit()

        for category in session.get("image_urls", {}):
            file_url = url_for("get_file", filename=img.name, _external=True)
            if file_url in session["image_urls"][category]:
                session["image_urls"][category].remove(file_url)
                session.modified = True

        return jsonify({"message": "Image deleted successfully"}), 200

    app.logger.error(f"Image not found in database: {filename}")
    return jsonify({"error": "Image not found"}), 404


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
        return redirect(url_for("login"))

    email = session.get("email")
    outfits = Outfit.query.filter_by(email=email).all()
    return render_template(
        "outfitgallery.html", username=session["username"], outfits=outfits
    )


@app.route("/community-page")
@app.route("/community-page.html")
def community_page():
    if "email" not in session or "username" not in session:
        return redirect(url_for("login"))
    username = session.get("username")
    return render_template("community-page.html", username=username)


@app.route("/outfitcreator", methods=["GET", "POST"])
@app.route("/outfitcreator.html", methods=["GET", "POST"])
def outfit_creator():
    if not session.get("email"):
        return redirect("/login")

    email = session.get("email")
    images = Img.query.filter_by(email=email).all()

    image_urls = {}
    for img in images:
        if Img.category not in image_urls:
            image_urls[Img.category] = []
        image_urls[Img.category].append(url_for("get_file", filename=Img.name))

    return render_template(
        "outfitcreator.html", image_urls=image_urls
    )

@app.route("/index", methods=["GET", "POST"])
@app.route("/index.html", methods=["GET", "POST"])
def index():
    form = UploadClothesForm()
    file_url = None
    email = session.get("email")

    if request.method == "POST" and form.validate_on_submit():
        if email:
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

    images = Img.query.filter_by(email=email).all() if email else []
    return render_template("index.html", form=form, file_url=file_url, images=images, username=session["username"])


@app.route("/uploads/<filename>")
def get_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/imgwindow/<filename>", methods=["GET", "POST"])
def imgwindow(filename):
    file_url = url_for("get_file", filename=filename)
    return render_template("imgwindow.html", file_url=file_url)


@app.route("/wardrobecategory", methods=["GET", "POST"])
@app.route("/wardrobecategory.html", methods=["GET", "POST"])
def wardrobecategory():
    if not session.get("email"):
        return redirect("/login")

    category = request.form.get('category')
    file_url = request.form.get('file_url')

    if 'image_urls' not in session:
        session['image_urls'] = {}

    if category not in session['image_urls']:
        session['image_urls'][category] = []
    
    session['image_urls'][category].append(file_url)
    session.modified = True

    return render_template('wardrobecategory.html', category=category, file_url=file_url, image_urls=session['image_urls'], username=session["username"])


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
