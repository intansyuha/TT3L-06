from flask import Flask, render_template, request, redirect

app = Flask(__name__)

<<<<<<< HEAD
# Dummy user database (replace this with your actual user database)
users = {
    "ali2": "pass123",
    "user2": "password2",
    "user3": "password3"
}
=======
app = Flask(__name__, static_folder='static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
>>>>>>> main

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/signup.html')
def signup():
    return render_template('signup.html')

@app.route('/login.html')
def login_redirect():
    return redirect('/')

@app.route('/login-email.html')
def login_email():
    return render_template('login-email.html')

if __name__ == '__main__':
    app.run(debug=True)
