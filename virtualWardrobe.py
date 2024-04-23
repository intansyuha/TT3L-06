from flask import Flask, render_template #to return actual files

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return "Hello from Flask"

if __name__ == '__main__':
    app.run(debug=True)