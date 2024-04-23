from flask import Flask, render_template #to return actual files
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
    if form.validate_on_submit():
        file = form.file.data # Grab file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename) # Save file
        file.save(file_path)
        mimetype = file.content_type
        with open(file_path, 'rb') as f:
            img_data = f.read()

        img = Img(data=img_data, mimetype=mimetype, name=filename)
        db.session.add(img)
        return "File has been uploaded"
    
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)