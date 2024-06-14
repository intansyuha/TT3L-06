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
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import FileField, SubmitField, SelectField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired
from db import db, init_db  # Import init_db to initialize the database
from rembg import remove
from models import db, User, Img, Outfit, Feed
from datetime import datetime
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
            ("bags", "Bags"),
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
            session["user_id"] = user.id
            session["username"] = user.username
            print(f"User {user.username} logged in successfully. Session: {session}")
            return redirect(url_for('community_page', username=user.username))
        else:
            flash("Invalid email or password", "error")
            print(f"Failed login attempt. Email: {email}")

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
  # Redirect to login after successful registration

    return render_template("signup.html")


@app.route("/save_outfit", methods=["POST"])
def save_outfit():
    try:
        data = request.get_json()
        app.logger.debug(f"Received data: {data}")

        data["user_id"] = session.get("user_id")
        if not data["user_id"]:
            return jsonify({"error": "Unauthorized"}), 401

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
    user_id = session.get("user_id")
    app.logger.debug(f"User ID from session: {user_id}")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    outfits = Outfit.query.filter_by(user_id=user_id).all()

    if not outfits:
        return jsonify({"message": "No outfits found for the specified user"}), 404

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
            # Delete associated images
            image_paths = [outfit.top, outfit.bottom, outfit.outerwear, outfit.shoes, outfit.bags, outfit.accessories]
            for image_path in image_paths:
                if image_path:
                    file_path = os.path.join(app.config["UPLOAD_FOLDER"], image_path)
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        print(f"Deleted file: {file_path}")
                    else:
                        print(f"File not found: {file_path}")

            # Delete outfit record from the database
            db.session.delete(outfit)
            db.session.commit()
            print(f"Outfit ID {outfit_id} deleted successfully.")
            return jsonify({"message": "Outfit deleted successfully"}), 200
        else:
            print(f"Outfit ID {outfit_id} not found.")
            return jsonify({"message": "Outfit not found"}), 404
    except Exception as e:
        app.logger.error(f"Error deleting outfit: {str(e)}")
        return jsonify({"error": "Failed to delete outfit"}), 400
    
@app.route("/delete_image/<filename>", methods=["DELETE"])
def delete_image(filename):
    user_id = session.get("user_id")
    if not user_id:
        app.logger.error("Unauthorized access attempt.")
        return jsonify({"error": "Unauthorized"}), 401

    app.logger.info(f"Attempting to delete image: {filename} for user: {user_id}")
    img = Img.query.filter_by(user_id=user_id, name=filename).first()
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

@app.route("/upload_outfit/<int:outfit_id>", methods=["POST"])
def upload_outfit(outfit_id):
    if "username" not in session:
        return jsonify({"message": "User not logged in"}), 401
    
    data = request.get_json()
    caption = data.get('caption')
    
    outfit = Outfit.query.get(outfit_id)
    if not outfit:
        return jsonify({"message": "Outfit not found"}), 404
    
    if outfit.user_id != session["user_id"]:
        return jsonify({"message": "Unauthorized action"}), 403
    
    # Create a new feed entry for the community page
    feed_entry = Feed(username=session["username"], outfit_id=outfit_id, caption=caption)
    db.session.add(feed_entry)
    db.session.commit()
    
    return jsonify({"message": "Outfit published successfully"}), 200

@app.route("/save-feed", methods=["POST"])
def save_feed():
    username = request.form.get("username")
    outfit_id = request.form.get("outfit_id")
    date = datetime.now()

    # Check if the username already exists in the feed table
    existing_feed = Feed.query.filter_by(username=username).first()
    
    if existing_feed:
        # Update the existing record
        existing_feed.outfit_id = outfit_id
        existing_feed.date = date
        db.session.commit()
        flash("Feed updated successfully!", "success")
    else:
        # Insert a new record
        new_feed = Feed(username=username, outfit_id=outfit_id, date=date)
        db.session.add(new_feed)
        db.session.commit()
        flash("Feed saved successfully!", "success")

    return redirect(url_for("community_page"))

@app.route("/update_outfit", methods=["POST"])
def update_outfit():
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ["id", "name", "top", "bottom", "outerwear", "shoes", "bags", "accessories"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        # Retrieve the outfit to be updated from the database
        user_id = session.get("user_id")
        outfit_id = data.get('id')
        outfit_name = data.get('name')
        outfit = Outfit.query.filter_by(user_id=user_id, id=outfit_id, name=outfit_name).first()
        if not outfit:
            return jsonify({"error": "Outfit not found"}), 404

        # Update the outfit with the new data
        outfit.name = data["name"]
        outfit.top = data["top"]
        outfit.bottom = data["bottom"]
        outfit.outerwear = data["outerwear"]
        outfit.shoes = data["shoes"]
        outfit.bags = data["bags"]
        outfit.accessories = data["accessories"]

        # Commit changes to the database
        db.session.commit()

        return jsonify({"message": "Outfit updated successfully"}), 200
    except Exception as e:
        app.logger.error(f"Error updating outfit: {str(e)}")
        return jsonify({"error": "Failed to update outfit"}), 500

@app.route("/community-page")
@app.route("/community-page.html")
def community_page():
    if "user_id" not in session:
        flash("You must be logged in to access the community page.", "error")
        return redirect(url_for("login"))

    username = session.get("username")
    print(f"Accessing community page. Username: {username}, Session: {session}")

    feeds = Feed.query.all()
    feed_data = []

    for feed in feeds:
        outfit = db.session.get(Outfit, feed.outfit_id)
        if outfit:
            feed_data.append(
                {
                    "username": feed.username,
                    "image": outfit.top,  # Use the URL stored in the database
                    "outfit_id": outfit.id,
                    "caption": feed.caption,
                    "date": feed.date,
                }
            )

    return render_template("community-page.html", username=username, feeds=feed_data)


@app.route("/outfit/<int:outfit_id>")
def outfit_detail(outfit_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    outfit = Outfit.query.get(outfit_id)
    if not outfit:
        flash("Outfit not found", "error")
        return redirect(url_for("community_page"))

    outfit_data = {
        "name": outfit.name,
        "top": outfit.top,  # Use the URL stored in the database
        "bottom": outfit.bottom,  # Adjust as necessary
        "outerwear": outfit.outerwear,
        "shoes": outfit.shoes,
        "bags": outfit.bags,
        "accessories": outfit.accessories,
    }

    return render_template("outfit_detail.html", username=session["username"], outfit=outfit_data)

@app.route("/outfitgallery")
@app.route("/outfitgallery.html")
def outfit_gallery():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session.get("user_id")
    outfits = Outfit.query.filter_by(user_id=user_id).all()
    return render_template(
        "outfitgallery.html", username=session["username"], outfits=outfits
    )

@app.route("/outfitcreator", methods=["GET", "POST"])
@app.route("/outfitcreator.html", methods=["GET", "POST"])
def outfit_creator():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))

    images = Img.query.filter_by(user_id=user_id).all()

    image_urls = {category: [] for category, _ in UploadClothesForm().category.choices}
    for img in images:
        image_urls[img.category].append(url_for("get_file", filename=img.name))

    return render_template(
        "outfitcreator.html", image_urls=image_urls, username=session["username"]
    )


@app.route("/index", methods=["GET", "POST"])
@app.route("/index.html", methods=["GET", "POST"])
def index():
    form = UploadClothesForm()
    file_url = None
    user_id = session.get("user_id")

    if request.method == "POST" and form.validate_on_submit():
        if user_id:
            file = form.file.data  # grab file
            filename = secure_filename(file.filename)
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
                user_id=user_id,
            )
            db.session.add(img)
            db.session.commit()

            # Update session with new image URL
            file_url = url_for("get_file", filename=filename, _external=True)
            if "image_urls" not in session:
                session["image_urls"] = {}

            if category not in session["image_urls"]:
                session["image_urls"][category] = []

            session["image_urls"][category].append(file_url)
            session.modified = True

        return redirect(url_for("wardrobecategory"))

    images = Img.query.filter_by(user_id=user_id).all() if user_id else []
    return render_template(
        "index.html",
        form=form,
        file_url=file_url,
        images=images,
        username=session["username"],
    )


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
    user_id = session.get("user_id")
    if not user_id:
        app.logger.debug("No user ID in session. Redirecting to login.")
        return redirect(url_for("login"))

    user = User.query.get(user_id)
    if not user:
        app.logger.debug(f"No user found with ID: {user_id}. Redirecting to login.")
        return redirect(url_for("login"))

    app.logger.debug(f"Current user ID: {user_id}")

    # Fetch images associated with the logged-in user's user_id
    images = Img.query.filter_by(user_id=user_id).all()
    app.logger.debug(f"Retrieved images: {[img.name for img in images]}")

    # Construct image URLs for each category
    image_urls = {category: [] for category, _ in UploadClothesForm().category.choices}
    for img in images:
        file_url = url_for("get_file", filename=img.name)
        image_urls[img.category].append(file_url)
        app.logger.debug(f"Added image URL: {file_url} for category: {img.category}")

    # Render the template with the image URLs
    return render_template(
        "wardrobecategory.html", image_urls=image_urls, username=session["username"]
    )

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
