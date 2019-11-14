import models

from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict


plant = Blueprint('plants', 'plant')

@plant.route('/', methods=['GET'])
def get_all_plants():
	try:
		plants = [model_to_dict(plant) for plant in models.Plant.select()]
		print(plants)
		return jsonify(data=plants, status={'code': 200, 'message': 'success'})
	except models.DoesNotExist:
		return jsonify(data={}, status={'code': 401, 'message': 'Error getting the resources'})

#define route to create a plant
@plant.route('/', methods=['POST'])
def create_plant():
	try:
		#this will get contain the info to create the plant
		payload = request.get_json()
		#**payload is the spread operator containing the new plants info
		plant = models.Plant.create(**payload)
		#turn the plant model into a dictionary 
		plant_dict = model_to_dict(plant)
		#return the jsonified object and a status code indicating sucess or error
		return jsonify(data=plant_dict, status={'code': 200, 'message': 'success'})
	except models.DoesNotExist:
		return jsonify(data={}, status={'code': 401, 'message': 'error getting the resources'})

#show a single plant by id
@plant.route('<id>', methods=['GET'])
#retrieve plant by id that is being passed down 
def get_one_plant(id):
	try:#if successful display found plants informtion
		plant = models.Plant.get_by_id(id)
		return jsonify(data=model_to_dict(plant), status={'code': 200, 'message': 'success'})
		#if unsuccessful return error message and no info
	except models.DoesNotExist:
		return jsonify(data={}, status={'code': 401, 'message': 'error getting thhe resources'})

#define route to update a plant by passing it's id through to the function
@plant.route('/<id>', methods=['PUT'])
def update_plant(id):
	try:
		payload = request.get_json()
		#query for specific plant that matches id being passed down and update it with new info from the payload
		query = models.Plant.update(**payload).where(models.Plant.id == id)
		query.execute()

		return jsonify(data=model_to_dict(models.Plant.get_by_id(id)), status={'code': 200, 'message': 'success'})
	except models.DoesNotExist:
		return jsonify(data={}, status={'code': 401, 'message': 'error getting the resources'})










