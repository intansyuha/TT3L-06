from flask import Flask, render_template, request, redirect

app = Flask(__name__)

app = Flask(__name__, static_folder='static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

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

@app.route('/forgot-password.html')
def forgot_password():
    return render_template('forgot-password.html')

if __name__ == '__main__':
    app.run(debug=True)
