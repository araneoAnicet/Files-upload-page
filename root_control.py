from objects_definitions import app
from flask import render_template, redirect, url_for, flash
from config import UPLOAD_FOLDER
from file_management import db, Image, file_upload, folder_content, remove_deleted_files
from api_management import add_resources


add_resources()  # adds API resources, definitions are in api_management.py

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/load', methods=['POST'])
def load():
    file_upload(db, Image, UPLOAD_FOLDER)
    flash('FILES WERE UPLOADED SUCCESSFULLY!')
    return redirect(url_for('index'))


@app.route('/images')
def images(api_option=None):
    return render_template('images.html', files=folder_content('static/' + UPLOAD_FOLDER + '/'))

@app.route('/api')
def api():
    return render_template('api_documentation.html')
    

if __name__ == '__main__':
    remove_deleted_files(db, Image, UPLOAD_FOLDER)  # optional: removes data of deleted files from database
    app.run(debug=True)