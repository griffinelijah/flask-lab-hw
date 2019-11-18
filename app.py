from flask import Flask, jsonify, g
from flask_cors import CORS

from flask_login import LoginManager

from resources.plants import plant

from resources.users import users

import models

DEBUG = True
PORT = 8000

app = Flask(__name__)

#set up session secret for login, we can update this to be more secure later
app.secret_key = 'super secret key oooooo'
#configure app to use login 
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
	try:#find userid from db that matches userid from input
		return models.User.get(models.User.id == userid)
	except models.DoesNotExist:
		return None



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
app.register_blueprint(users, url_prefix='/api/v1/users')

if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)
