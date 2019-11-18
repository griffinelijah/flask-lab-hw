import models
from flask import request, jsonify, Blueprint
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from playhouse.shortcuts import model_to_dict

#make a blueprint for the users
users = Blueprint('users', 'users')

@users.route('/register', methods=['POST'])
def register():
	payload = request.get_json()
	#lowercase the email to avoid dupes
	payload['email'].lower()

	try:#first check to see if users email exists in db
		models.User.get(models.User.email == payload['email'])
		#if it does return message saying the email is already registered
		return jsonify(data={}, status={'code': '401', 'message': 'A user with the email is already registered'})
	#if email does not exist continue with user registration
	except models.DoesNotExist:
		#here we are encrypting the pw with bcrypt
		payload['password'] = generate_password_hash(payload['password'])
		#create user in DB with info from payload
		user = models.User.create(**payload)
		#sign int he user
		login_user(user)
		user_dict = model_to_dict(user)
		#remove password before sending back response to client
		del user_dict['password']

		return jsonify(data=user_dict,status={'code': 201, 'message': 'succesfully registered {}'.format(user_dict['email'])}), 201

@users.route('/login', methods=['POST'])
def login():
	payload = request.get_json()
	try: #look up user by their email
		user = models.User.get(models.User.email == payload['email'])
		user_dict = model_to_dict(user)
		#check their password hash
		if(check_password_hash(user_dict['password'], payload['password'])):
			#if pw matches log them in
			login_user(user)
			#delete pw from dict before returning
			del user_dict['password']
			return jsonify(data=user_dict, status={'code': 200, 'message': 'succesfully loggined in {}'.format(user_dict['email'])}), 200
		else:
			#if pw does not match, print internal log and return invlaid message
			print('password no good')
			return jsonify(data={}, status={'code': 401, 'message': 'Username or Password is incorrect'}), 401

	except models.DoesNotExist:
		print('email not found')
		return jsonify(data={}, status={'code': 401, 'message': 'username or password is incorrect'}), 401







