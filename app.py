from flask import Flask, render_template, request, redirect, session, jsonify, flash, url_for, send_from_directory
from flask_wtf import FlaskForm
from flask_login import LoginManager, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import FileField, SubmitField, SelectField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired
from db import db, User
from rembg import remove
from models import Img, Outfit
import os
import bcrypt
from PIL import Image

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'clothesuploadkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/files'
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'app.login'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class UploadClothesForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    category = SelectField("Category", choices=[("top", "Top"), ("bottom", "Bottom"), ("outerwear", "Outerwear"), ("shoes", "Shoes"), ("accessories", "Accessories")], validators=[InputRequired()])
    submit = SubmitField("Upload File")

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
            session['username'] = user.username
            return redirect(url_for('community_page', username=user.username))

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
    if 'email' not in session:
        return redirect(url_for('login'))
    return render_template('community-page.html', username=session['username'])

@app.route('/outfitcreator')
@app.route('/outfitcreator.html')
def outfit_creator():
    if 'email' not in session:
        return redirect(url_for('login'))
    return render_template('outfitcreator.html', username=session['username'])

@app.route('/outfitgallery')
@app.route('/outfitgallery.html')
def outfit_gallery():
    if 'email' not in session:
        return redirect(url_for('login'))
    return render_template('outfitgallery.html', username=session['username'])

@app.route('/settings')
@app.route('/settings.html')
def settings():
    if 'email' not in session:
        return redirect(url_for('login'))
    return render_template('settings.html', username=session['username'])

@app.route('/index', methods=['GET', "POST"])
@app.route('/index.html', methods=['GET', "POST"])
def index():
    form = UploadClothesForm()
    file_url = None
    if form.validate_on_submit():
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
