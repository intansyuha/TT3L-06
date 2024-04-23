from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(8), nullable=False)
    password = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(50), nullable=False)

# Create tables
db.create_all()

@app.route('/')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_submit():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    
    # Create a new user instance
    new_user = User(username=username, password=password, email=email)
    
    # Add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    
    return redirect(url_for('success'))

@app.route('/success')
def success():
    return "Sign Up Successful!"

if __name__ == '__main__':
    app.run(debug=True)
