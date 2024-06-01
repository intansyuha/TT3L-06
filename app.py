from flask import Flask, render_template, request, redirect, session, jsonify, flash, url_for
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import os

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'secret_key'

app.config['MYSQL_USERNAME'] = ""
app.config['MYSQL_EMAIL'] = ""
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = ""

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(8), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(50))

    def __init__(self, email, password, username):
        self.username = username
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
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

if __name__ == '__main__':
    app.run(debug=True)
