import os
from datetime import datetime
from flask import request
from datetime import datetime

SECRET = 'H@xwaid2q8YH@IYE*(hfWI#NO:#@(S!OSjfa'
IMG_FOLDER = 'static/stored_images/'

def file_upload(upload_path):
    target = os.path.join(os.path.dirname(os.path.abspath(__file__)), upload_path)
    if not os.path.isdir(target):
        os.mkdir(target)
    for file in request.files.getlist('file'):
        print('\nLOADING .  .   .   .  {}'.format(file.filename))
        print('    UPLOAD DATE:     {}'.format(str(datetime.now())))
        modified_name = datetime.today().strftime('%Y-%m-%d-%H:%M:%s') + '___' + file.filename
        destination = '/'.join([target, modified_name])
        file.save(destination)
    print('.    .   .   .FILES UPLOADED  .   .   .   .\n')

def folder_content(link='static/stored_images/'):
    if not os.path.exists(link):
        return None
    for img_name in os.listdir(link):
        yield link + img_name
