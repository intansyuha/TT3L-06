from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'secret_key'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(8), nullable=False)
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
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['username'] = user.username
            session['password'] = user.password
            return redirect('/community-page')
        else:
            return render_template('login.html', error='Invalid username')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
@app.route('/signup.html', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # handle request
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')

    return render_template('signup.html')

@app.route('/login-email', methods=['GET', 'POST'])
@app.route('/login-email.html', methods=['GET', 'POST'])
def login_email():
    if request.method == 'POST':
        # handle request
        pass

    return render_template('login-email.html')

@app.route('/forgot-password')
@app.route('/forgot-password.html')
def forgot_password():
    return render_template('forgot-password.html')

@app.route('/community-page')
@app.route('/community-page.html')
def community_page():
    if session['username']:
        return render_template('community-page.html')
    
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
