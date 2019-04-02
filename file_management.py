from werkzeug.utils import secure_filename
from flask import request
from objects_definitions import db
from hashlib import sha256
from random import randint
from base64 import b64encode, b64decode
from datetime import datetime
import os


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    hash = db.Column(db.String, nullable=False)
    folder = db.Column(db.String(50), nullable=False)
    
    def __repr__(self):
        return '{}  {}  {}'.format(self.id, self.name, self.date)


def file_upload(database, dataclass, directory, randomability=20000):
    new_files_list = []
    folder_file = 'static/' + directory + '/'
    if not os.path.isdir(folder_file):
        os.mkdir(folder_file)
    for file in request.files.getlist('file'):
        img_name = secure_filename(file.filename)
        img_hashed_name = sha256(bytes(img_name + str(randint(0, randomability)), 'utf-8')).hexdigest()
        new_img = dataclass(name=img_name, hash=img_hashed_name, folder = directory)
        database.session.add(new_img)
        new_files_list.append(new_img)

        file.save(os.path.join(folder_file, img_hashed_name))
        print('>>SAVING ' + img_hashed_name )
    print('.    .   .   FILES LOADED    .   .   .')
    database.session.commit()
    return new_files_list

def remove_deleted_files(database, dataclass, directory):
    folder = 'static/' + directory + '/'
    current_files_hash = [img for img in folder_files(folder)]
    files_to_remove = [element for element in dataclass.query.all() if element.hash not in current_files_hash]
    for element in files_to_remove:
        database.session.delete(element)
    database.session.commit()

def get_by_id(dataclass, search_id):
    return dataclass.query.filter_by(id=search_id)

def get_by_hash(dataclass, search_hash):
    return dataclass.query.filter_by(hash=search_hash).first()

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