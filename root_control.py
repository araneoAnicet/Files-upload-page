from objects_definitions import app
from flask import render_template, redirect, url_for, flash, request, jsonify
from config import UPLOAD_FOLDER, API_UPLOAD_FOLDER
from file_management import file_upload, folder_content, folder_files, folders_check
import os


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
@app.route('/api/images', methods=['POST'])
def api_post_image():
    saved_files = [filename for filename in file_upload(API_UPLOAD_FOLDER)]
    if saved_files:
        return jsonify({
            'message': '{} images were uploaded successfully'.format(len(saved_files)),
            'status': 200,
            'data': list(map(lambda img_hash: {'hash': img_hash} , saved_files)),
            'request_payload': {
                'url': '/api/images',
                'method': 'POST',
                'headers': None
            }
        })
    return jsonify({
        'message': 'No images were selected',
        'status': 404,
        'data': None,
        'request_payload': {
            'url': '/api/images',
            'method': 'POST',
            'headers': None
        }
    })

@app.route('/api/images', methods=['GET'])
def api_get_grid():
    grid_files = [filename for filename in folder_files('static/' + API_UPLOAD_FOLDER + '/')]
    if grid_files:
        return jsonify({
            'message': 'Returned {} images'.format(len(grid_files)),
            'status': 200,
            'data': list(map(lambda img_hash: {'hash': img_hash} , grid_files)),
            'request_payload': {
                'url': '/api/images',
                'method': 'GET',
                'headers': None
                }
        })
    return jsonify({
            'message': 'No images found',
            'status': 404,
            'data': None,
            'request_payload': {
                'url': '/api/images',
                'method': 'GET',
                'headers': None
                }
        })


@app.route('/api/images/<hash>', methods=['GET'])
def api_get_img(hash):
    if folder_files('static/' + API_UPLOAD_FOLDER + '/' + hash):
        return jsonify({
            'massage': 'Returned image',
            'status': 200,
            'data': {'hash': hash},
            'request_payload': {
                'url': '/api/images/' + hash,
                'method': 'GET',
                'headers': None
                }
        })
    return jsonify({
        'message': 'Image was not found',
        'status': 404,
        'data': None,
        'request_payload': {
            'url': '/api/images/' + hash,
            'method': 'GET',
            'headers': None
            }
    })
    
@app.route('/api/images/<hash>', methods=['DELETE'])
def api_delete_img(hash):
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
        'data': None,
        'request_payload': {
            'url': '/api/images' + hash,
            'method': 'DELETE',
            'headers': None
        }
    })

if __name__ == '__main__':
    folders_check([UPLOAD_FOLDER, API_UPLOAD_FOLDER])
    app.run(debug=True)