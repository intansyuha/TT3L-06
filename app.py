from flask import Flask, render_template, request, redirect, session, jsonify, flash, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from wtforms.validators import InputRequired
from flask_wtf import FlaskForm
from wtforms import FileField, SelectField,  SubmitField
from werkzeug.utils import secure_filename
from models import User, Img, Outfit
import os

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/files'
db = SQLAlchemy(app)
app.secret_key = 'secret_key'

app.config['MYSQL_USERNAME'] = ""
app.config['MYSQL_EMAIL'] = ""
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = ""
    
class UploadClothesForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

def create_db():
    with app.app_context():
        db.create_all()
    
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Check if the user exists and password matches
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['email'] = email
            session['password'] = password
            return render_template('community-page.html')

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
            return jsonify({'error': 'Username or email already exists'}), 400
        else:
            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful!', 'success')
            return render_template('/')
    
    return render_template('signup.html')

@app.route('/community-page')
@app.route('/community-page.html')
def community_page():
    if session['email']:
        return render_template('community-page.html')
    
    return redirect('/login')

@app.route('/settings', methods=['GET', 'POST'])
@app.route('/settings.html', methods=['GET', 'POST'])
def settings():
    if session['email']:
        return render_template('settings.html')
    
    return redirect('/login')

@app.route("/outfitcreator")
@app.route("/outfitcreator.html")
def outfitcreator():
    if session['email']:
        return render_template('outfitcreator.html')
    
    return redirect("/login")


@app.route("/outfitgallery")
@app.route("/outfitgallery.html")
def outfit_gallery():
    if session['email']:
        return render_template('outfitgallery.html')
    
    return redirect("/login")

@app.route('/imgwindow', methods=['GET', "POST"])
@app.route('/imgwindow.html', methods=['GET', "POST"])
def home():
    if session['email']:
        form = UploadClothesForm()
        file_url = None
        if form.validate_on_submit():
            file = form.file.data # grab file
            filename = secure_filename(file.filename)
            file_url = url_for('get_file', filename=filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename) # save file
            file.save(file_path)
            mimetype = file.content_type
            with open(file_path, 'rb') as f:
                img_data = f.read()

            img = Img(data=img_data, mimetype=mimetype, name=filename)
            db.session.add(img)

            return redirect(url_for('imgwindow', filename=filename))
    
    return render_template('index.html', form=form, file_url=file_url)

@app.route('/uploads/<filename>')
def get_file(filename):
     return redirect(app.config['UPLOAD_FOLDER'], filename)


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

@app.route('/imgwindow', methods=['GET', "POST"])
@app.route('/imgwindow.html', methods=['GET', "POST"])
def home():
    form = UploadClothesForm()
    file_url = None
    if form.validate_on_submit():
        file = form.file.data # grab file
        filename = secure_filename(file.filename)
        file_url = url_for('get_file', filename=filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename) # save file
        file.save(file_path)
        mimetype = file.content_type
        with open(file_path, 'rb') as f:
            img_data = f.read()

        img = Img(data=img_data, mimetype=mimetype, name=filename)
        db.session.add(img)

        return redirect(url_for('imgwindow', filename=filename))
    
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
