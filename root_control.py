from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from config import IMG_FOLDER, SECRET, file_upload, folder_content

app = Flask(__name__)
app.secret_key = SECRET
Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/load', methods=['POST'])
def load():
    file_upload(IMG_FOLDER)
    flash('FILES WERE UPLOADED SUCCESSFULLY!')
    return redirect(url_for('index'))


@app.route('/images', methods=['GET'])
def images():
    return render_template('images.html', files=folder_content())

if __name__ == '__main__':
    app.run(debug=True)