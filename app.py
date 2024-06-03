from flask import Flask, render_template, request, redirect, session, jsonify, flash, url_for, send_from_directory
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, SelectField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired
from db import db, User
from models import Img, Outfit
import os
import bcrypt
from PIL import Image

app = Flask(__name__, static_folder='static')
app.secret_key = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/files'

class UploadClothesForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    category = SelectField("Category", choices=[("top", "Top"), ("bottom", "Bottom"), ("outerwear", "Outerwear"), ("shoes", "Shoes"), ("accessories", "Accessories")], validators=[InputRequired()])
    submit = SubmitField("Upload File")

with app.app_context():
    db.init_app(app)
    db.create_all()

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
            flash('Username or email already exists', 'error')
            return render_template('signup.html')  # Re-render the signup form with error message
        else:
            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)
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
    if session.get('email'):
        return render_template('settings.html')

    return redirect('/login')

@app.route('/outfitcreator')
@app.route('/outfitcreator.html')
def outfit_creator():
    if not session.get('email'):
        return redirect('/login')
    
    return render_template('outfitcreator.html')

@app.route('/outfitgallery')
@app.route('/outfitgallery.html')
def outfit_gallery():
    if not session.get('email'):
        return redirect('/login')
    
    return render_template('outfitgallery.html')

@app.route('/index', methods=['GET', 'POST'])
@app.route('/index.html', methods=['GET', 'POST'])
def index():
    form = UploadClothesForm()
    file_url = None

    if request.method == 'POST' and form.validate_on_submit():
        if session.get('email'):
            try:
                file = form.file.data
                filename = secure_filename(file.filename)
                file_url = url_for('get_file', filename=filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                mimetype = file.content_type

                with open(file_path, 'rb') as f:
                    img_data = f.read()

                img = Img(data=img_data, mimetype=mimetype, name=filename)
                db.session.add(img)
                db.session.commit()

                return redirect(url_for('imgwindow', filename=filename))
            except Exception as e:
                flash(f'An error occurred: {str(e)}', 'error')

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

if __name__ == '__main__':
    app.run(debug=True)
