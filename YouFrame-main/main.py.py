import os
from flask import Flask, redirect, render_template, request
from werkzeug.utils import secure_filename
from werkzeug import exceptions

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Extensiones de archivo permitidas

app = Flask(__name__)
app.config['UPLOAD_PATH'] = 'static/uploads'


def allowed_file(filename):
    # Verificar si la extensión del archivo es válida
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def uploader():
    path = 'static/uploads/'
    uploads = sorted(os.listdir(path), key=lambda x: os.path.getctime(path + x))
    uploads = ['uploads/' + file for file in uploads]
    uploads.reverse()
    return render_template("index.html", uploads=uploads)


@app.route("/upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        else:
            raise exceptions.BadRequest("Me quieres nagualiar perro, solo puedes subir archivos que sean de fotos")
        return redirect("/")


if __name__ == "__main__":
    app.run()
