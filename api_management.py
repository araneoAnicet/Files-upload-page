from flask import request
from objects_definitions import api, db
from flask_restful import Resource, reqparse
from file_management import Image, get_by_hash, file_upload
import os

class ImagesApi(Resource):
    def get(self):
        return {'images': 
                    tuple(map(lambda image: 
                        {
                        'id': image.id,
                        'name': image.name,
                        'posted': str(image.date),
                        'folder': image.folder
                        }, Image.query.all())), 
                'status': 'OK'}, 200


class GridApi(Resource):
    def post(self, folder):
        received_images = file_upload(db, Image, folder)
        if received_images:
            return {'images': 
                        tuple(map(lambda image: 
                            {
                            'id': image.id,
                            'name': image.name,
                            'posted': str(image.date),
                            'folder': image.folder,
                            'hash': image.hash
                            }, received_images)), 
                    'status': 'OK'}, 200
        return {'status': 'No Files'}, 404

class ImageApi(Resource):
    def get(self, image_hash):
        image = get_by_hash(Image, image_hash)
        return {
    'id': image.id, 
    'name': image.name, 
    'posted': str(image.date), 
    'folder': image.folder, 
    'status': 'OK'}, 200 

    def delete(self, image_hash):
        image = get_by_hash(Image, image_hash)
        os.remove('static/' + image.folder + '/' + image_hash)
        response = {
            'id': image.id,
            'name': image.name,
            'posted': str(image.date),
            'folder': image.folder,
            'status': 'OK'
            }
        db.session.delete(image)
        db.session.commit()
        return response, 200


def add_resources():
    api.add_resource(ImagesApi, '/api/images', endpoint='grid')
    api.add_resource(ImageApi, '/api/images/<image_hash>', endpoint='def_img')
    api.add_resource(GridApi, '/api/add/<folder>', endpoint='add')

if __name__ == '__main__':
    print('it works!')