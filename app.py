from flask import Flask, escape, request, render_template, flash, redirect, url_for
from pdf2image import convert_from_path
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
UPLOAD_FOLDER = 'G:/PDF_converter/upload/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
SAVE_FOLDER = 'G:/PDF_converter/save'
app.config['SAVE_FOLDER'] = SAVE_FOLDER
ALLOWED_EXTENSIONS = {'pdf'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method.lower() == 'get':
        return render_template('home.html')
    elif request.method.lower() == 'post':
        if 'file' not in request.files:
            return 'no part'
        files = request.files.getlist('file')

        # submit an empty part without filename
        for file in files:
            if file.filename == '':
                return 'No selected file'
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                images_from_path = convert_from_path(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                for i, page in enumerate(images_from_path):
                    page.save(f'''{os.path.join(app.config['SAVE_FOLDER'], f"{filename.rsplit('.', 1)[0].lower()}{str(i)}")}{'.bmp'}''')

        return 'success'



if __name__ == "__main__":
    app.run(debug=True)
