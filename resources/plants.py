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
	except models.DoesNotExist;
		return jsonify(data={}, status={'code': 401, 'message': 'Error getting the resources'})