from objects_definitions import app
from flask import render_template, redirect, url_for, flash, request, jsonify
from config import UPLOAD_FOLDER, API_UPLOAD_FOLDER, ADMIN, JWT_KEY
from file_management import file_upload, folder_content, folder_files, folders_check
import jwt
from datetime import datetime, timedelta
import os
from functools import wraps

def token_req(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        token = request.headers['Authorization']
        if not token:
            return jsonify({
            'message': 'Token is missing',
            'status': 404,
            'data': None,
            'request_payload': {
                'token': None,
                'url': None,
                'method': None,
                'headers': dict(request.headers)
            }
        }), 404
        try:
            decoded_token = jwt.decode(token, JWT_KEY)
            return func(*args, **kwargs)
        except Exception as error:
            print(error)
            return jsonify({
            'message': 'Invalid token',
            'status': 403,
            'data': None,
            'request_payload': {
                'token': token,
                'url': None,
                'method': None,
                'headers': dict(request.headers)
            }
        }), 403
    return decorator

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
@app.route('/api/get_token', methods=['GET', 'POST'])
def get_token():
    user_data = request.get_json()
    if 'username' in user_data and 'password' in user_data:
        if user_data['username'] == ADMIN['username'] and user_data['password'] == ADMIN['password']:
            token = jwt.encode(
                {
                    'username': ADMIN['username'],
                    'is_admin': True,
                    'exp': datetime.utcnow() + timedelta(days=1)
                    }, JWT_KEY)

            return jsonify({
            'message': 'Authorized successfully',
            'status': 200,
            'data': {'token': token.decode('utf-8')},
            'request_payload': {
                'request': user_data,
                'url': '/api/get_token',
                'method': 'POST',
                'headers': dict(request.headers)
            }
        }), 403
        else:
            return jsonify({
            'message': 'Incorrect username or password',
            'status': 403,
            'data': None,
            'request_payload': {
                'request': user_data,
                'url': '/api/get_token',
                'method': 'POST',
                'headers': dict(request.headers)
            }
        }), 403

    return jsonify({
            'message': 'No username or password',
            'status': 404,
            'data': None,
            'request_payload': {
                'request': user_data,
                'url': '/api/get_token',
                'method': 'POST',
                'headers': dict(request.headers)
            }
        }), 404      
    

@app.route('/api/images', methods=['POST'])
@token_req
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
                'headers': dict(request.headers)
            }
        }), 200
    return jsonify({
        'message': 'No images were selected',
        'status': 404,
        'data': None,
        'request_payload': {
            'url': '/api/images',
            'method': 'POST',
            'headers': dict(request.headers)
        }
    }), 404

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
                'headers': dict(request.headers)
                }
        }), 200
    return jsonify({
            'message': 'No images found',
            'status': 404,
            'data': None,
            'request_payload': {
                'url': '/api/images',
                'method': 'GET',
                'headers': dict(request.headers)
                }
        }), 404


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
                'headers': dict(request.headers)
                }
        }), 200
    return jsonify({
        'message': 'Image was not found',
        'status': 404,
        'data': None,
        'request_payload': {
            'url': '/api/images/' + hash,
            'method': 'GET',
            'headers': dict(request.headers)
            }
    }), 404
    
@app.route('/api/images/<hash>', methods=['DELETE'])
@token_req
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
                'headers': dict(request.headers)
                }
        }), 200
    return jsonify({
        'message': 'Image was not found',
        'status': 404,
        'data': None,
        'request_payload': {
            'url': '/api/images' + hash,
            'method': 'DELETE',
            'headers': dict(request.headers)
        }
    }), 404

if __name__ == '__main__':
    folders_check([UPLOAD_FOLDER, API_UPLOAD_FOLDER])  # optional
    app.run(debug=True)