from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dummy user database (replace this with your actual user database)
users = {
    "user1": "password1",
    "user2": "password2",
    "user3": "password3"
}

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if username in users and users[username] == password:
        # Successful login, redirect to the dashboard
        return redirect(url_for('dashboard'))
    else:
        # Failed login, render the login page with an error message
        return render_template('login.html', error='Invalid username or password')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
