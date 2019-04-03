from flask import Flask
from config import SECRET
from flask_cors import CORS
from flask_bootstrap import Bootstrap
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

CORS(app)
api = Api(app)
# JWT / Bearer token 

#token dostepu w jwt 

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.secret_key = SECRET
Bootstrap(app)