from flask import Flask, render_template, request, redirect, session, jsonify, flash, url_for, send_from_directory
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, SelectField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired
from db import db, User
from rembg import remove
from models import Img, Outfit
import os
import bcrypt
from PIL import Image
from rembg import remove
import io

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'clothesuploadkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/files'
db.init_app(app)

class UploadClothesForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    category = SelectField("Category", choices=[("top", "Top"), ("bottom", "Bottom"), ("outerwear", "Outerwear"), ("shoes", "Shoes"), ("accessories", "Accessories")], validators=[InputRequired()])
    submit = SubmitField("Upload File")


class CreateOutfitForm(FlaskForm):
    top = SelectField("Top", coerce=int)
    bottom = SelectField("Bottom", coerce=int)
    shoes = SelectField("Shoes", coerce=int)
    outerwear = SelectField("Outerwear", coerce=int)
    bag = SelectField("Bag", coerce=int)
    submitOF = SubmitField("Save Outfit")
    publish = SubmitField("Publish Outfit")


def combine_images(images):
    widths, heights = zip(*(i.size for i in images))
    total_width = max(widths)
    total_height = sum(heights)

    combined_image = Image.new("RGB", (total_width, total_height))
    y_offset = 0
    for img in images:
        combined_image.paste(img, (0, y_offset))
        y_offset += img.height

    return combined_image


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['email'] = email
            session['password'] = password
            return redirect(url_for('community_page'))

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
@app.route('/signup.html', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()

        if existing_user:
            flash('Username or email already exists.', 'error')
            return render_template('signup.html')  # Re-render the signup form with error message
        else:
            current_user = User(username=username, email=email, password=password)
            db.session.add(current_user)
            db.session.commit()
            flash('Registration successful!', 'success')
            return redirect('/login')  # Redirect to login after successful registration

    return render_template('signup.html')

@app.route('/community-page')
@app.route('/community-page.html')
def community_page():
    if session.get('email'):
        return render_template('community-page.html')

    return redirect('/login')

@app.route('/settings')
@app.route('/settings.html')
def settings():
    if request.method == 'POST':
        new_username = request.form['new_username']
        new_email = request.form['new_email']
        new_password = request.form['new_password']

        existing_user = User.query.filter((User.username == new_username) | (User.email == new_email)).first()
        
        if existing_user:
            flash('Username or email already exists.', 'error')
            return render_template('/settings.html')  # Re-render the signup form with error message
        else:
            new_user = User(username=new_username, email=new_email, password=new_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful!', 'success')
            return redirect('/settings.html')
    
    return render_template('/settings.html')

@app.route('/outfitcreator')
@app.route('/outfitcreator.html')
def outfit_creator():
    if not session.get('email'):
        return redirect('/login')

    return render_template('outfitcreator.html')


@app.route("/create_outfit", methods=["GET", "POST"])
def create_outfit():
    form = CreateOutfitForm()

    # Populate the form with image choices
    form.top.choices = [
        (img.id, img.name) for img in Img.query.filter_by(category="top").all()
    ]
    form.bottom.choices = [
        (img.id, img.name) for img in Img.query.filter_by(category="bottom").all()
    ]
    form.shoes.choices = [
        (img.id, img.name) for img in Img.query.filter_by(category="shoes").all()
    ]
    form.outerwear.choices = [
        (img.id, img.name) for img in Img.query.filter_by(category="outerwear").all()
    ]
    form.bag.choices = [
        (img.id, img.name) for img in Img.query.filter_by(category="accessories").all()
    ]

    if form.validate_on_submit():
        top = Img.query.get(form.top.data)
        bottom = Img.query.get(form.bottom.data)
        shoes = Img.query.get(form.shoes.data)
        outerwear = Img.query.get(form.outerwear.data)
        bag = Img.query.get(form.bag.data)

        images = [
            Image.open(io.BytesIO(img.data))
            for img in [top, bottom, shoes, outerwear, bag]
        ]
        combined_image = combine_images(images)

        img_byte_arr = io.BytesIO()
        combined_image.save(img_byte_arr, format="JPEG")
        img_byte_arr = img_byte_arr.getvalue()

        new_outfit = Outfit(
            data=img_byte_arr,
            mimetype="image/jpeg",
            published="publish" in request.form,
        )

        db.session.add(new_outfit)
        db.session.commit()

        flash("Outfit saved successfully!", "success")
        return redirect(url_for("outfit_gallery"))

    return render_template("create_outfit.html", form=form)


@app.route('/outfitgallery')
@app.route('/outfitgallery.html')
def outfit_gallery():
    if not session.get('email'):
        return redirect('/login')
    
    return render_template('outfitgallery.html')

@app.route('/index', methods=['GET', "POST"])
@app.route('/index.html', methods=['GET', "POST"])
def index():
    form = UploadClothesForm()
    file_url = None
    if request.method == 'POST' and form.validate_on_submit():
        if session.get('email'):
            file = form.file.data # grab file
            filename = secure_filename(file.filename)
            file_url = url_for('get_file', filename=filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename) # save file
            file.save(file_path)

            with open(file_path, 'rb') as input_file:
                input_data = input_file.read()

            output_data = remove(input_data)


            process_filename = filename
            process_file_path = os.path.join(app.config['UPLOAD_FOLDER'], process_filename)

            with open(process_file_path, 'wb') as output_file:
                output_file.write(output_data)

            mimetype = file.mimetype


            img = Img(data=output_data, mimetype=mimetype, name=filename)
            db.session.add(img)
            db.session.commit()

            return redirect(url_for('imgwindow', filename=process_filename))
    return render_template('index.html', form=form, file_url=file_url)


@app.route('/uploads/<filename>')
def get_file(filename):
     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/imgwindow/<filename>', methods=['GET', 'POST'])
def imgwindow(filename):
    file_url = url_for('get_file', filename=filename)
    return render_template('imgwindow.html', file_url=file_url)

@app.route('/wardrobecategory/', methods=['POST'])
def wardrobecategory():
    category = request.form.get('category')
    file_url = request.form.get('file_url')

    if 'image_urls' not in session:
        session['image_urls'] = {}

    if category not in session['image_urls']:
        session['image_urls'][category] = []
    
    session['image_urls'][category].append(file_url)
    session.modified = True

    return render_template('wardrobecategory.html', category=category, file_url=file_url, image_urls=session['image_urls'])

def create_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    from models import Img
    create_db()
    app.run(debug=True)
