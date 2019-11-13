from flask import Flask, jsonify, g
from flask_cors import CORS

from resources.plants import plant

import models

DEBUG = True
PORT = 8000

app = Flask(__name__)

CORS(plant, origins=['http://localhost:3000'], supports_credentials=True)

app.register_blueprint(plant, url_prefix='/	api/v1/plants')