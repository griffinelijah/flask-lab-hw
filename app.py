from flask import Flask, jsonify, g
from flask_cors import CORS

from resources.plants import plant

import models

DEBUG = True
PORT = 8000

app = Flask(__name__)

@app.before_request
def before_request():
	g.db = models.DATABASE
	g.db.connect()

@app.after_request
def after_request(response):
	g.db.close()
	return response

CORS(plant, origins=['http://localhost:3000'], supports_credentials=True)

app.register_blueprint(plant, url_prefix='/api/v1/plants')

if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)
