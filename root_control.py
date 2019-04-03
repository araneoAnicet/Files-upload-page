from objects_definitions import app, json_response
from flask import render_template, redirect, url_for, flash, request, jsonify
from config import UPLOAD_FOLDER, API_UPLOAD_FOLDER
from file_management import file_upload, folder_content
import os
#from api_management import add_resources


#add_resources()  # adds API resources, definitions are in api_management.py

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/load', methods=['POST'])
def load():
    file_upload(db, Image, UPLOAD_FOLDER)
    flash('FILES WERE UPLOADED SUCCESSFULLY!')
    return redirect(url_for('index'))


@app.route('/images')
def images():
    return render_template('images.html', files=folder_content('static/' + UPLOAD_FOLDER + '/'))


@app.route('/api')
def api():
    return render_template('api_documentation.html')


# REST
@app.route('/api/images/<hash>', methods=['GET'])
def api_image(hash):
    if folder_files('static/' + API_UPLOAD_FOLDER + '/' + hash):
        return jsonify({
            'massage': 'Returned images',
            'status': 200,
            'data': {'hash': hash},
            'request_payload': {'url': '/api/images/' + hash}
        })
    return jsonify({
        'message': 'Image was not found',
        'status': 404,
        'data': {'hash': hash},
        'request_payload': {
            'url': '/api/images/' + hash,
            'method': 'GET',
            'headers': None
            }
    })
    
@app.route('/api/images/<hash>', methods=['DELETE'])
def api_image(hash):
    if folder_files('static/uploads' + hash):
        os.remove('static/' + API_UPLOAD_FOLDER + '/' + hash)
        return jsonify({
            'message': 'Image was deleted successfully',
            'status': 200,
            'data': {'hash': hash},
            'request_payload': {
                'url': '/api/images/' + hash,
                'method': 'DELETE',
                'headers': None
                }
        })
    return jsonify({
        'message': 'Image was not found',
        'status': 404,
        'data': {'hash': hash},
        'request_payload': {
            'url': '/api/images' + hash,
            'method': 'DELETE',
            'headers': None
        }
    })

if __name__ == '__main__':
    app.run(debug=True)