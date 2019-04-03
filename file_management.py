from werkzeug.utils import secure_filename
from flask import request
import os


def file_upload(directory):
    saved_files = []
    folder_file = 'static/' + directory + '/'
    if not os.path.isdir(folder_file):
        os.mkdir(folder_file)
    for file in request.files.getlist('file'):
        secure_name = secure_filename(file.filename)
        file.save(os.path.join(folder_file, secure_name))
        saved_files.append(secure_name)
    return saved_files

def folder_files(link):
    if not os.path.exists(link):
        return None
    for file_name in os.listdir(link):
        yield file_name

def folder_content(link):
    for img_name in folder_files(link):
        yield link + img_name


if __name__ == '__main__':
    print('It works!')