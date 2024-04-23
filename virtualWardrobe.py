from flask import Flask, render_template #to return actual files
from flask_wtf import FlaskForm
from wtforms import FileField,  SubmitField
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'clothesuploadkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

class UploadClothesForm(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Upload File")

@app.route('/', methods=['GET', "POST"])
@app.route('/home', methods=['GET', "POST"])
def home():
    form = UploadClothesForm()
    if form.validate_on_submit():
        file = form.file.data # Grab file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # Save file
        return "File has been uploaded"
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)