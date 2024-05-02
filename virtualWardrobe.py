from flask import Flask, redirect, render_template, send_from_directory, url_for # to return actual files
from flask_wtf import FlaskForm
from wtforms import FileField,  SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
from db import db_init, db
from models import Img



app = Flask(__name__)
app.config['SECRET_KEY'] = 'clothesuploadkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///img.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/files'
db_init(app)

class UploadClothesForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route('/', methods=['GET', "POST"])
@app.route('/home', methods=['GET', "POST"])
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
        db.session.commit()

        return redirect(url_for('get_file', filename=filename))
    
    return render_template('index.html', form=form, file_url=file_url)


@app.route('/uploads/<filename>')
def get_file(filename):
    return render_template('imgwindow.html', filename=filename)

def create_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    from models import Img
    create_db()
    app.run(debug=True)